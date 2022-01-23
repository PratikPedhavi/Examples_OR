'''
    You have three currency denominations with 11 coins each. The total worth (of all 11 coins) 
    is 15 bits for denomination 1, 16 bits for denomination 2 and 17 bits for denomination 3. 
    You need to buy one 11-bit item. Use ILP to determine the smallest number of coins of the 
    three denominations needed to make the purchase.
'''

from ortools.sat.python import cp_model

def main():
    denom_values = [15, 16, 17]
    number_deno = 3
    model =  cp_model.CpModel()    
    x = {}
    for idx in range(number_deno):
        x[idx] = model.NewIntVar(0, 11, '{}'.format(idx))

    # CONSTRAINTS
    model.Add(sum([deno * x[idx] for idx, deno in enumerate(denom_values)]) == 121)

    model.Minimize(sum([x[idx] for idx in range(number_deno)]))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for idx in range(number_deno):
            print(' {} coins of denomination {}'.format(solver.Value(x[idx]), idx+1))
        print('Total coins used: {}'.format(solver.ObjectiveValue()))

if __name__ == '__main__':
    main()


