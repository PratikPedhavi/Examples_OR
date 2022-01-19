'''
    The Record-a-song company has contracted with a rising star to record eight songs. 
    The sizes in MB of the different songs are 8, 3, 5, 5, 9, 6, 7, and 12 resp. Record-a-song 
    uses two CDs for the recording. Each CD has a capacity of 30 MB. The compaany would like to
    distribute the songs between the two CDs such that the used space on each CD is about the same. 
    Formulate the problem as an ILP and find the optimum solution.

    Extended:
    Suppose that the nature of the melodies dictates that songs 3 and 4 cannot be recorded on the same CD. 
    Formulate the problem as an ILP. Would it be possible to use a 25 MB CD to record the eight songs? 
    If not use ILP to determine the minimum CD capacity needed to make the recording.
'''

from ortools.sat.python import cp_model

def main():
    song_size = [8, 3, 5, 5, 9, 6, 7, 12]
    number_cds = 2
    # cd_capacity = 25

    model = cp_model.CpModel()

    # VARIABLES
    x = {}
    for song in range(len(song_size)):
        for cd in range(number_cds):
            x[song, cd] = model.NewBoolVar('{}_{}'.format(song, cd))

    diff = model.NewIntVar(0, 10, 'diff')
    cd_capacity = model.NewIntVar(0, 30, 'capacity')

    # CONSTRAINTS

    for song, size_s in enumerate(song_size):
        model.Add(sum([x[song, cd] for cd in range(number_cds)]) == 1)

    size_1 = sum([size_s * x[song, 0] for song, size_s in enumerate(song_size)])
    size_2 = sum([size_s * x[song, 1] for song, size_s in enumerate(song_size)])
    model.Add(size_1 <= cd_capacity)
    model.Add(size_2 <= cd_capacity)
    model.Add(size_1 - size_2 == diff)

    # Extra constraints 
    for cd in range(number_cds):
        model.Add(x[2, cd] + x[3, cd] <= 1)
    

    model.Minimize(diff+cd_capacity)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        group_1 = ''
        group_2 = ''
        group_1_sum = 0
        group_2_sum = 0
        for song, size in enumerate(song_size):
            if solver.BooleanValue(x[song,0]):
                group_1 += '{} ({} MB), '.format(1+song, size)
                group_1_sum += size
            if solver.BooleanValue(x[song,1]):
                group_2 += '{} ({} MB), '.format(1+song, size)
                group_2_sum += size
        print('Group 1 songs: {}'.format(group_1))
        print('Group 2 songs: {}'.format(group_2))
        print('Group 1 total: {}'.format(group_1_sum))
        print('Group 2 total: {}'.format(group_2_sum))
        print('Minimum capacity needed: {}'.format(solver.Value(cd_capacity)))

if __name__ == '__main__':
    main()

