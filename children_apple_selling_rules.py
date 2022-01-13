'''
    Three children go to the market to sell 90 apples.
    karen carries 50 apples, Bill 30 and John 10. 
    Five rules from their parents:
    1. The selling price is either 1$ for 7 apples or 3$ for 1 apple or a combination of the two prices.
    2. Each child may exercise one or both options of the selling price.
    3. Each of the three children must return with exactly the same amount of money.
    4. Each childs income must be in whole dollars 
    5. The amount received by each child must be the largest possible under the stipulated conditions.
    Assume that the three kids are able to sell all they have.
'''

from ortools.sat.python import cp_model

def main():
    model = cp_model.CpModel()

    # Data
    children = ['Karen', 'Bill', 'John']
    apple_count = [50, 30, 10]

    # Variables - amount of type 1 and type 2 transactions by each child
    type1 = {}
    type2 = {}
    for child in children:
        type1[child] = model.NewIntVar(0, 10, '{}_1'.format(child))
        type2[child] = model.NewIntVar(0, 10, '{}_2'.format(child))
    individual_income = model.NewIntVar(0,500,'income')
    
    # Constraints
    # Quantity conservation
    for num, child in enumerate(children):
        model.Add(7 * type1[child] + 1 * type2[child] == apple_count[num])
    
    for num, child in enumerate(children):
        model.Add(1 * type1[child] + 3 * type2[child] == individual_income)
    
    model.Maximize(individual_income)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for num, child in enumerate(children):
            print('For {}'.format(child))
            print('Apples sold - Type 1 : {} and Type 2 : {}'.format(7*solver.Value(type1[child]), 1*solver.Value(type2[child])))
            print('Income earned - Type 1 : {} + Type 2 : {} = {}'.format(solver.Value(type1[child]), 
                                                                    3*solver.Value(type2[child]), solver.Value(individual_income)))
            print()

if __name__ == '__main__':
    main()