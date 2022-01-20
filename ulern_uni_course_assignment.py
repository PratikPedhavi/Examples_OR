'''
    Ulern university uses a mathematical model that optimizes student preferences taking into account the limitation of classroom 
    and faculty resources. To demonstrate the application of the model, consider the simplified case of 10 students who are 
    required to select two courses out of six offered electives. The table below gives scores that represent each students's 
    preference for individual courses, with a score of 100 behing highest. For simplicity, it is assumed that the preference 
    score for a two-course selection is the sum of the individual score. Course capacity is the maximum number of students allowed 
    to take the class.
    Formulate the problem as an ILP and find the optimum solution. 

'''

from ortools.sat.python import cp_model

def get_data_model():
    data = {}
    data['pref_score'] = [
        [20, 40, 50, 30, 90, 100],
        [90, 00, 80, 70, 10, 40],
        [25, 40, 30, 80, 30, 40],
        [80, 50, 60, 80, 30, 40],
        [75, 60, 90, 100, 50, 40],
        [60, 40, 90, 10, 80, 80],
        [45, 40, 70, 60, 55, 60],
        [30, 100,  40, 70, 90, 55],
        [80, 60, 100, 70, 65, 80],
        [40, 60, 80, 100, 90, 10]
    ]
    data['course_capacity'] = [6, 8, 5, 5, 6, 5]
    return data

def main():
    data = get_data_model()
    students = len(data['pref_score'])
    courses = len(data['pref_score'][0])

    model = cp_model.CpModel()

    x = {}
    for student in range(students):
        for course in range(courses):
            x[student, course] = model.NewBoolVar('{}_{}'.format(student, course))

    # CONSTRAINTS 
    for student in range(students):
        model.Add(sum([x[student, course] for course in range(courses)]) == 2)

    for course in range(courses):
        model.Add(sum([x[student, course] for student in range(students)]) <= data['course_capacity'][course])

    weighted_sum = [data['pref_score'][student][course] * x[student, course] for student in range(students) for course in range(courses)]
    model.Maximize(sum(weighted_sum))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        total_score = 0
        for student in range(students):
            student_courses = ''
            for course in range(courses):
                if solver.BooleanValue(x[student, course]):
                    score = data['pref_score'][student][course]
                    student_courses += '{} ({}), '.format(course, score)
                    total_score += score
            print('Student {} studies {}'.format(student, student_courses))
        print('Total Score: {}'.format(solver.ObjectiveValue()))

if __name__ == '__main__':
    main()