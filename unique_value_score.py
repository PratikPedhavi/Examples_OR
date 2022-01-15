'''
    Group 1 : {set of words}
    Group 2 : {set of words}

    All the words in group 1 and 2 can be formed from the nine letteres A, E, F, H, O, P, R, S and T. Develop a model to assign
     a unique numeric value from 1 through 9 to these letters such that the difference between the total scores of the two groups
     will be as small as possible. 
'''

from ortools.sat.python import cp_model

def main():
    group_1 = ['AREA', 'FORT', 'HOPE', 'SPAR', 'THAT', 'TREE']
    group_2 = ['ERST', 'FOOT', 'HEAT', 'PAST', 'PROF', 'STOP']
    unique_letters = ['A', 'E', 'F', 'H', 'O', 'P', 'R', 'S', 'T']

    model = cp_model.CpModel()

    # VARIABLES
    x = {}
    for letter in unique_letters:
        for num in range(1,10):
            x[letter,num] = model.NewBoolVar('{}_{}'.format(letter, num))

    sum_1 = sum([num * x[k,num] for word in group_1 for k in word for num in range(1,10)])
    sum_2 = sum([num * x[k,num] for word in group_2 for k in word for num in range(1,10)])

    # VARIABLES
    # Only one value per character
    for letter in unique_letters:
        model.Add(sum([x[letter, num] for num in range(1,10)]) == 1)

    for num in range(1,10):
        model.Add(sum([x[letter,num] for letter in unique_letters]) == 1)

    # OBJECTIVE VALUE
    model.Maximize(sum_1 - sum_2)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE :
        output = 'Optimal solution: \n'
        output += '{'
        for letter in unique_letters:
            for num in range(1,10):
                if solver.BooleanValue(x[letter,num]):
                    output += ' {} : {}, '.format(letter, num)
        output += ' }'
        print(output)
        print('Objective Value : {}'.format(solver.ObjectiveValue()))

if __name__ == "__main__":
    main()