'''
    Given i = 1, 2, ..., n, formulate a general ILP model (for any n) to determine th e smallest number y that, when divided by the 
    integer amount 2+i, will always produce a remainder equal to i; that is , y mod (2 + i) = i.
'''

from ortools.sat.python import cp_model

def main(n):
    Y_LIMIT = 5000 # DEPENDS ON n
    model = cp_model.CpModel()

    y = model.NewIntVar(1, Y_LIMIT, 'smallest_mod')
    m = {}
    for k in range(n):
        m[k] = model.NewIntVar(1, Y_LIMIT, 'multiple_{}'.format(k))

    # CONSTRAINTS 
    for k in range(n):
        model.Add(m[k] * (2 + (k + 1)) + (k+1) == y)

    model.Minimize(y)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Minimum y value is {}'.format(solver.Value(y)))

if __name__ == '__main__':
    main(3)