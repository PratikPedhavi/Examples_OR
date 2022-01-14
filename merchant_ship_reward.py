'''
    Once upon a time there was a captain of a merchant ship who wanted to reward three crew members for their 
    valiant effort in saving the ship's cargo during an unexpected storm in the high seas. The captain put aside a 
    certain sum of money in the pursers's office and instructed the first officer to distribute it equally 
    among the three mariners after the ship reached shore. 
    One night one of the sailors unbeknown to others, went to the pursers's office and decided to claim one-third 
    of the money in advance. After he had divided the money into three equal shares, an extra coin remained which 
    the mariner decided to keep. 
    The next night, the second mariner got the same idea and repeating the same three- way division with what was left 
    ended up keeping an extra coin as well. The third night, the third mariner also took a third of what was left 
    plus an extra coin that could not be divided. 
    When the ship reached shore the first officer divided what was left of the money equally among the three mariners 
    again to be left with an extra coin. To simplify things the first officer put the extra coin aside and gave the 
    three mariners their allotted equal shares. How much money was in the safe to start with? Formulate the problem
    as an ILP and find the solution. 
'''

from ortools.sat.python import cp_model

def main():
    model = cp_model.CpModel()

    x = {}
    x[1] = model.NewIntVar(0,1000,'night_1')
    x[2] = model.NewIntVar(0,1000,'night_2')
    x[3] = model.NewIntVar(0,1000,'night_3')
    x[4] = model.NewIntVar(0,1000,'harbour')
    z = model.NewIntVar(0,10000,'total')

    # CONSTRAINTS
    # Night One
    model.Add(3 * x[1] + 1 == z)
    # Night Two
    model.Add(3 * x[2] + 1 == z - (x[1] + 1))
    # Night Three
    model.Add(3 * x[3] + 1 == z - (x[1] + x[2] + 2))
    # At harbour
    model.Add(3 * x[4] + 1 == z - (x[1] + x[2] + x[3] + 3))
    
    # OBJECTIVE
    model.Minimize(z)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    print(status)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Amount removed on 1st night: {} + 1'.format(solver.Value(x[1])))
        print('Amount removed on 2nd night: {} + 1'.format(solver.Value(x[2])))
        print('Amount removed on 3rd night: {} + 1'.format(solver.Value(x[3])))
        print('Amount received per mariner at harbor: {}'.format(solver.Value(x[4])))
        print("Total initial sum: {}".format(solver.ObjectiveValue()))

if __name__ == '__main__':
    main()