'''
    7 full wine bottles, 7 half-full and 7 empty bottles. Divide the 21 bottles among 3 individuals
    such that each receives exactly 7. Additionally, each individual must receive equal quantity of 
    wine. Express as ILP problem and find the solution.
'''

from ortools.sat.python import cp_model

def main():
    model = cp_model.CpModel()

    bottle_quant = [1, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0, 0, 0, 0]
    bottle_quant = [2*k for k in bottle_quant]
    num_individual = 3

    # CONSTRAINTS
    x = {}
    for i in range(num_individual):
        for k in range(len(bottle_quant)):
            x[i,k] = model.NewBoolVar('x[{},{}]'.format(i,k))
    
    # 7 bottles per individual
    for i in range(num_individual):
        model.Add(sum([x[i,k] for k in range(len(bottle_quant))]) == 7)

    #  A bottle allocated at max to only one person
    for k in range(len(bottle_quant)):
        model.Add(sum([x[i,k] for i in range(num_individual)]) == 1)

    # All individuals get same quantity
    quantity_1 = sum([bottle_quant[k] * x[0,k] for k in range(len(bottle_quant))])
    quantity_2 = sum([bottle_quant[k] * x[1,k] for k in range(len(bottle_quant))])
    quantity_3 = sum([bottle_quant[k] * x[2,k] for k in range(len(bottle_quant))])
    model.Add(quantity_1 - quantity_2 == 0)
    model.Add(quantity_2 - quantity_3 == 0)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for i in range(num_individual):
            Total_quant = 0
            for k in range(len(bottle_quant)):
                if solver.BooleanValue(x[i,k]):
                    Total_quant += bottle_quant[k]/2
                    print('Bottle {} ({}) is assigned to person {}'.format(k,bottle_quant[k]/2,i))
            print('Total Quantity assigned to person {} is {}'.format(i, Total_quant))

if __name__ == '__main__':
    main()

