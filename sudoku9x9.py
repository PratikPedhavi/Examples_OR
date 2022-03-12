'''
    The world renowned Japanese logic puzzle, Sudoku, deals with a 9 x 9 grid subdivide into 9 nonoverlapping 3 x 3 subgrids. 
    The puzzle calls for assigning the numerical digits 1 through 9 to the cells of the grid such that ech row, each column, 
    and each subgrid contain distinct digits.Some of the cells may be fixed in advance. 
    Formulate the problem as an integer program, and find the solution for the instance given below.
'''

from pkgutil import get_data
from ortools.sat.python import cp_model

def get_data_model():
    data = {
        (0,1):6, (0,3):1, (0,5):4, (0,7):5,
        (1,2):8, (1,3):3, (1,5):5, (1,6):6,
        (2,0):2, (2,6):7,
        (3,0):8, (3,3):4, (3,5):7, (3,8):6,
        (4,2):6, (4,6):3,
        (5,0):7, (5,3):9, (5,5):1, (5,8):4,
        (6,0):5, (6,8):2,
        (7,2):7, (7,3):2, (7,5):6, (7,6):9,
        (8,1):4, (8,3):5, (8,5):8, (8,7):7
    }
    return data

def get_data_model_4():
    data = {
        (0,0):1, (0,3):4,
        (1,1):4, (1,2):1,
        (2,1):3, (2,2):2,
        (3,0):2, (3,3):3
    }
    return data

def main(n,m):
    data = get_data_model()

    model = cp_model.CpModel()

    # VARIABLES
    x = {}
    for i in range(n):
        for j in range(n):
            for k in range(1,n+1):
                if tuple([i,j]) in data.keys():
                    if data[(i,j)] == k:
                        x[i,j,k] = 1
                        continue
                x[i,j,k] = model.NewBoolVar('{}_{}_{}'.format(i,j,k))
                # if tuple([i,j]) in data.keys():
                #     if data[(i,j)] == k:
                #         model.AddAbsEquality(x[i,j,k],1)
    
    
    # CONSTRAINTS
    # rows

    # for i in range(n):
    #     model.Add(sum([x[i,j,k] for j in range(n) for k in range(1,n+1)]) == n)

    # # columns
    # for j in range(n):
    #     model.Add(sum([x[i,j,k] for i in range(n) for k in range(1,n+1)]) == n)

    for j in range(n):
        for k in range(1,n+1):
            model.Add(sum([x[i,j,k] for i in range(n)]) == 1)

    for i in range(n):
        for k in range(1,n+1):
            model.Add(sum([x[i,j,k] for j in range(n)]) == 1)

    for i in range(n):
        for j in range(n):
            model.Add(sum([x[i,j,k] for k in range(1,n+1)]) == 1)

    # subgrid 
    for a in range(m):
        for b in range(m):
            for k in range(1,n+1):
                z,y = a*m, b*m
                grid_1 = sum([x[i,j,k] for i in range(z,z+m) for j in range(y,y+m)])
                model.Add(grid_1 == 1)
    
    model.Minimize(0)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    print(status)
    print()

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        output = ''
        for i in range(n):
            for j in range(n):
                for k in range(1,n+1):
                    if solver.Value(x[i,j,k]):
                        output += '{} \t'.format(k)
            output += '\n'
        
        print(output)
        return

if __name__ == '__main__':
    main(9,3)