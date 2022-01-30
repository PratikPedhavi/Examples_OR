'''
    A widely circulated puzzlw requires assigning a single distinct digit (0 through 9) to each letter in the equation
    SEND + MORE = MONEY. Formulate the problem as an integer program and find the solution. 
    (Hint: This is an assignment model with side conditions.)
'''

from ortools.sat.python import cp_model

def main():
    letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
    possible_values = range(10)

    model = cp_model.CpModel()

    x = {}
    for letter in letters:
        for val in possible_values:
            x[letter, val] = model.NewBoolVar('{}_{}'.format(letter, val))

    # CONSTRAINTS

    for letter in letters:
        model.Add(sum([x[letter, val] for val in possible_values]) == 1)

    for val in possible_values:
        model.Add(sum([x[letter, val] for letter in letters]) <= 1)

    int_val = {}
    for letter in letters:
        int_val[letter] = sum([val * x[letter, val] for val in possible_values])
    
    send_val = 1000*int_val['S'] + 100*int_val['E'] + 10*int_val['N'] + int_val['D']
    more_val = 1000*int_val['M'] + 100*int_val['O'] + 10*int_val['R'] + int_val['E']
    money_val = 10000*int_val['M'] + 1000*int_val['O'] + 100*int_val['N'] + 10*int_val['E'] + int_val['Y']

    model.Add(send_val + more_val == money_val)

    model.Minimize(0)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        output_val = {}
        for letter in letters:
            for val in possible_values:
                if solver.BooleanValue(x[letter,val]):
                    output_val[letter] = val                    

        output = ''
        vals = ''
        for letter in 'SEND':
            output += '{}'.format(letter)
            vals += '{}'.format(output_val[letter])
        output += '\t ({})'.format(vals)
        output += '+ \n'
        vals = ''
        for letter in 'MORE':
            output += '{}'.format(letter)
            vals += '{}'.format(output_val[letter])
        output += '\t ({})'.format(vals)
        output += '= \n'
        vals = ''
        for letter in 'MONEY':
            output += '{}'.format(letter)
            vals += '{}'.format(output_val[letter])
        output += '\t ({})'.format(vals)
        print(output)

if __name__ == '__main__':
    main()