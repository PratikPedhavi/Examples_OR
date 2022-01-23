'''
    You have a 4 x 4 grid and a total of 10 tokens. Use ILP to place the tokens on the grid such that 
    each row and each column will have an even number of tokens.
'''
from ortools.sat.python import cp_model

def main():
    grid_size = 4
    tokens = 10
    
    model = cp_model.CpModel()

    x = {}
    n = {}
    for row in range(grid_size):
        for col in range(grid_size):
            x[row, col] = model.NewBoolVar('{}_{}'.format(row, col))
        n[row] = model.NewIntVar(0, 4, '{}'.format(row))
    for col in range(grid_size):
        n[col] = model.NewIntVar(0, 4, '{}'.format(col))

    for row in range(grid_size):
        model.Add(sum([x[row, col] for col in range(grid_size)]) == 2*n[row])
    
    for col in range(grid_size):
        model.Add(sum([x[row, col] for row in range(grid_size)]) == 2*n[col])
    
    model.Add(sum([x[row, col] for row in range(grid_size) for col in range(grid_size)]) == 10)

    model.Minimize(0)
    # print(model.Proto())

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Output: \n')
        output = ''
        for row in range(grid_size):
            for col in range(grid_size):
                output += '{} '.format(solver.Value(x[row, col]))
            output += '\n'
        print(output)

if __name__ == '__main__':
    main()

    
    