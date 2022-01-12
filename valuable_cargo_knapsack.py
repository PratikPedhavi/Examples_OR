'''
    Five items are to be loaded in a vessel. The weight volume and value are given.
    The maximum allowable cargo weight and volume are 112 tons and 109 yd3, resp. 
    Formulate the ILP model and find the most valuable cargo.
'''

from ortools.sat.python import cp_model

def get_data_model():
    data = {}
    data['unit_weight'] = [5, 8, 3, 2, 7]
    data['unit_volume'] = [1, 8, 6, 5, 4]
    data['unit_worth'] = [4, 7, 6, 5, 4]
    data['max_weight'] = 112
    data['max_volume'] = 109
    return data

def main():
    data = get_data_model()

    model = cp_model.CpModel()

    num_items = len(data['unit_weight'])
    
    # VARIABLES
    x = {}
    for k in range(num_items):
        x[k] = model.NewIntVar(0,25,'x[{}]'.format(k))

    # CONSTRAINTS
    sum_weight = sum([i * x[k] for k, i in enumerate(data['unit_weight'])])
    model.Add(sum_weight <= data['max_weight'])

    sum_volume = sum([i * x[k] for k, i in enumerate(data['unit_volume'])])
    model.Add(sum_volume <= data['max_volume'])

    # OBJECTIVE
    objective_term = [i * x[k] for k,i in enumerate(data['unit_worth'])]
    model.Maximize(sum(objective_term))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for item in range(num_items):
            if solver.BooleanValue(x[item]):
                print('{} quantities of item {} is added in the vessel'.format(solver.Value(x[item]), item+1))
        print('Total worth: {}'.format(solver.ObjectiveValue()))

if __name__ == '__main__':
    main()