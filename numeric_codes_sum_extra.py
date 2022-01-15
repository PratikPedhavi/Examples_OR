'''
    You have the following three letter words: 
    APT, FAR, TVA, ADV, JOE, FIN, OSF and KEN. 
    Suppose that we assign numeric values to the alphabet starting with A=1 and ending with Z=26. 
    Each word is scored by  adding numeric codes of its three letters. Ex. AFT scores = 1+6+20 = 27
    You have to select five of the eight words that yield the maximum total score.
    The selected words must satisfy the following constraints.
    (Sum of letter 1 scores) < (Sum of letter 2 scores) < (Sum of letter 3 scores)

    formulate and find optimal solution.
    Additional constraint: The sum of column 1 and the sum of column 2 will be largest as well.
'''

import string
from ortools.sat.python import cp_model

def main():
    model = cp_model.CpModel()

    # PREPROCESSING
    alphabets = list(string.ascii_uppercase)
    map_alpha = {k:i+1 for i,k in enumerate(alphabets)}

    def score(code):
        return sum({map_alpha[k] for k in list(code)})
    
    # DATA
    words = ['APT', 'FAR', 'TVA', 'ADV', 'JOE', 'FIN', 'OSF', 'KEN']
    scores = [score(word) for word in words]

    # VARIABLES
    x = {}
    y = {}
    for k,word in enumerate(words):
        x[k] = model.NewBoolVar(word)
        for i,letter in enumerate(list(word)):
            y[k,i] = model.NewBoolVar('{}_{}'.format(k,i))

    # CONSTRAINTS
    model.Add(sum([x[k] for k in range(len(words))]) == 5)

    for k in range(len(words)):
        for i in range(len(words[k])):
            model.Add(y[k,i] == x[k])

    # inequality constraint    
    sum_1 = sum([map_alpha[words[k][0]] * y[k,0] for k in range(len(words))])
    sum_2 = sum([map_alpha[words[k][1]] * y[k,1] for k in range(len(words))])
    sum_3 = sum([map_alpha[words[k][2]] * y[k,2] for k in range(len(words))])
    model.Add(sum_1 + 1 <= sum_2)
    model.Add(sum_2 + 1 <= sum_3)

    score_sum = sum([scores[k] * x[k] for k in range(len(words))])
    model.Maximize(score_sum + sum_1 + sum_2)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        sum_1 = 0
        sum_2 = 0
        sum_3 = 0
        selected_words = []
        for k,word in enumerate(words):
            if solver.BooleanValue(x[k]):
                temp = '{} ({}) '.format(word, scores[k])
                selected_words.append(temp)
                sum_1 += map_alpha[word[0]]
                sum_2 += map_alpha[word[1]]
                sum_3 += map_alpha[word[2]]
        print('Top 5 words are: ',selected_words, '\n')
        print('Sum of all first elements {} < second element {} < third element {}'.format(sum_1, sum_2, sum_3))
        print('Total score: {}'.format(solver.ObjectiveValue()))

if __name__ == '__main__':
    main()