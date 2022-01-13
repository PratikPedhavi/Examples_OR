'''
    Sheikh left a will to distibute a herd of camels. 
    Tarek receives at least one-half of the herd.
    Sharif receives at least one-third of the herd.
    Maisa gets at least one-ninth of the herd.
    The remainder goes to charity.
    Given: total camel count is an odd number, charity receives exactly one camel.
'''

from ortools.sat.python import cp_model

def main():
    model = cp_model.CpModel()

    x = model.NewIntVar(0, 100, 'x')
    y = model.NewIntVar(0, 100, 'y')
    Tarek = model.NewIntVar(0, 100, 'tar')
    Sharif = model.NewIntVar(0, 100, 'sha')
    Maisa = model.NewIntVar(0, 100, 'mai')

    # CONSTRAINTS
    model.Add(2 * Tarek >= x)
    model.Add(3 * Sharif >= x)
    model.Add(9 * Maisa >= x)
    # Conservation constraint
    model.Add(Tarek + Sharif + Maisa + 1 == x)
    # Odd number constraint
    model.Add(x == 2*y+1)

    model.Minimize(0)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Total number of columns: {}'.format(solver.Value(x)))
        print('Camels for Tarek: {}'.format(solver.Value(Tarek)))
        print('Camels for Sharif: {}'.format(solver.Value(Sharif)))
        print('Camels for Maisa: {}'.format(solver.Value(Maisa)))

if __name__ == '__main__':
    main()