''' Five Projects are being evaluated over a 3-year planning horizon. Which project
    should be selected?
 '''

from ortools.sat.python import cp_model
import numpy as np

def get_data_model():
    data = {}
    data['expenditure'] = [
        [5,1,8],
        [4,7,10],
        [3,9,2],
        [7,4,1],
        [8,6,10]
    ]
    data['returns'] = [20, 40, 20, 15, 30]
    data['funds'] = [25, 25, 25]
    return data

def main():
    data = get_data_model()

    num_projects = len(data['expenditure'])

    model = cp_model.CpModel()

    # VARIABLES
    x = {}
    for k in range(num_projects):
        x[k] = model.NewBoolVar('x[{}]'.format(k))

    # CONSTRAINTS
    expenditure_yearly = np.transpose(data['expenditure'])
    for k, i in enumerate(expenditure_yearly):
        model.Add(sum([item * x[key] for key,item in enumerate(i)]) <= data['funds'][k])

    # Project 5 is selected if either of project 1 or 3 is selected
    model.Add(x[0] <= x[4])
    model.Add(x[2] <= x[4])

    # Project 2 & 3 are mutually exclusive
    model.Add(x[2] + x[3] <= 1)

    # OBJECTIVE
    model.Maximize(sum([data['returns'][k] * x[k] for k in range(num_projects)]))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for project in range(num_projects):
            if solver.BooleanValue(x[project]):
                print('Project {} is selected!'.format(project))
        print('Total Returns: ', solver.ObjectiveValue())
    return

if __name__ == '__main__':
    main()