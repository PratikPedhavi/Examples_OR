'''
    A street vendor selling electronic gadgets was robbed of all his possessions. When reporting the matter to the police, the
    vendor did not know the number of gadgets he had but stated that when dividing the total in lots of size 2, 3, 4, 5 or 6, 
    there was always one gadget left over. On the other hand, there was no remainder when the total was divided into lots of size
    7. Use ILP to determine the total number of gadgets the vendor had.
'''

from ortools.sat.python import cp_model

def main():
    undivisible = [2, 3, 4, 5, 6]

    model = cp_model.CpModel()

    # The variable that represents the actual number of gadgets
    x = model.NewIntVar(0, 500, 'x')

    # The multiples for each undivisible number
    n = {}
    for num in range(len(undivisible)):
        n[num] = model.NewIntVar(0,500,'{}'.format(num))
    n['div'] = model.NewIntVar(0,500,'{}'.format('div'))

    # UNDIVISIBLE CONSTRAINTS
    for num, val in enumerate(undivisible):
        model.Add(n[num]*val + 1 == x)
    
    # DIVISIBLE CONSTRAINTS
    model.Add(n['div'] * 7 == x)

    model.Minimize(x)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('The total number of gadgets were {}'.format(solver.Value(x)))

if __name__ == '__main__':
    main()