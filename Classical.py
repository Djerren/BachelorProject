# Classical.py consists of all the necessary function to calculate the probability of the best
# classical strategy for LSSD with three parties and |X| = |A| = |B| = |C|.

import numpy as np
from math import sqrt
import matplotlib.pyplot as plt

# these four functions represent each of the possible binary functions.
def id_func(bit):
    return bit

def not_func(bit):
    return (bit + 1) % 2

def bot(bit):
    return 0

def top(bit):
    return 1

def find_win_prob(f, g, h, subset):
    """
    This function returns the winning probability of a classical strategy given by 3 binary functions.
    subset is a list of tuples, where each tuple is a possible combination of choices from the set X, A, B and C
    and the probability distribution is assumed to be uniform over this subset.
    """
    win_prob = 0

    # For each combination in subset, the game is won if all three guesses (determined by the three binary functions)
    # are the same as the first element x. We count the number of combinations in the subset for which the game is won.
    for element in subset:
        if element[0] == f(element[1]) == g(element[2]) == h(element[3]):
            win_prob += 1

    # The probability that the game is won given the subset and the strategy is given by the number of combinations
    # in the subset for which the game is won divided by the number of combination in the subset, because uniform
    # distribution is assumed.
    return win_prob/len(subset)

def find_optimal_strategy(subset):
    """
    This function receives a game, defined by the subset and finds the winning probability of the best
    deterministic strategy.
    """

    max_win_prob = 0
    bin_funcs = [id_func, not_func, bot, top]

    # We loop over all possible strategies and determine their win probability, if this probability
    # exceeds the current best probability, we replace the best win probability by this one
    for f in bin_funcs:
        for g in bin_funcs:
            for h in bin_funcs:
                win_prob = find_win_prob(f,g,h, subset)

                if win_prob > max_win_prob:
                    max_win_prob = win_prob
    return max_win_prob

def single_game():
    possible_combinations = [(0,0,0,0), (0,0,0,1), (0,0,1,0), (0,0,1,1),
                             (0,1,0,0), (0,1,0,1), (0,1,1,0), (0,1,1,1),
                             (1,0,0,0), (1,0,0,1), (1,0,1,0), (1,0,1,1),
                             (1,1,0,0), (1,1,0,1), (1,1,1,0), (1,1,1,1)]


    for i in range(1, 2**16):
        subset_string = '{0:016b}'.format(i)

        subset = []
        for j in range(16):
            if subset_string[j] == '1':
                subset.append(possible_combinations[j])
        max_win_prob = find_optimal_strategy(subset)
        if max_win_prob < 0.5:
            print(max_win_prob)

def distribution_matrix2(alpha):
    distribution = np.zeros((4,4,4))
    for output in range(4):
        for input1 in range(4):
            for input2 in range(4):
                value = 1/4
                if output == 0:
                    for thing in [input1, input2]:
                        if thing == 0:
                            value *= (1-alpha)**2
                        elif thing == 1 or thing == 2:
                            value *= alpha *(1-alpha)
                        else:
                            value *= alpha**2
                elif output == 1:
                    for thing in [input1, input2]:
                        if thing == 1:
                            value *= (1-alpha)**2
                        elif thing == 0 or thing == 3:
                            value *= alpha *(1-alpha)
                        else:
                            value *= alpha**2
                elif output == 2:
                    for thing in [input1, input2]:
                        if thing == 2:
                            value *= (1-alpha)**2
                        elif thing == 0 or thing == 3:
                            value *= alpha *(1-alpha)
                        else:
                            value *= alpha**2
                else:
                    for thing in [input1, input2]:
                        if thing == 3:
                            value *= (1-alpha)**2
                        elif thing == 1 or thing == 2:
                            value *= alpha *(1-alpha)
                        else:
                            value *= alpha**2
                distribution[output][input1][input2] = value
    return distribution

def distribution_matrix3(alpha):
    distribution = np.zeros((8,8,8))
    for output in range(8):
        for input1 in range(8):
            for input2 in range(8):
                value = 1/8
                if output == 0:
                    for thing in [input1, input2]:
                        if thing == 0:
                            value *= (1-alpha)**3
                        elif thing == 1 or thing == 2 or thing == 4:
                            value *= alpha * (1-alpha)**2
                        elif thing == 3 or thing == 5 or thing == 6:
                            value *= (alpha**2) * (1-alpha)
                        else:
                            value *= alpha**3
                if output == 1:
                    for thing in [input1, input2]:
                        if thing == 1:
                            value *= (1-alpha)**3
                        elif thing == 0 or thing == 3 or thing == 5:
                            value *= alpha * (1-alpha)**2
                        elif thing == 2 or thing == 4 or thing == 7:
                            value *= (alpha**2) * (1-alpha)
                        else:
                            value *= alpha**3
                if output == 2:
                    for thing in [input1, input2]:
                        if thing == 2:
                            value *= (1-alpha)**3
                        elif thing == 3 or thing == 6 or thing == 0:
                            value *= alpha * (1-alpha)**2
                        elif thing == 1 or thing == 7 or thing == 4:
                            value *= (alpha**2) * (1-alpha)
                        else:
                            value *= alpha**3
                if output == 3:
                    for thing in [input1, input2]:
                        if thing == 3:
                            value *= (1-alpha)**3
                        elif thing == 7 or thing == 1 or thing == 2:
                            value *= alpha * (1-alpha)**2
                        elif thing == 5 or thing == 6 or thing == 0:
                            value *= (alpha**2) * (1-alpha)
                        else:
                            value *= alpha**3
                if output == 4:
                    for thing in [input1, input2]:
                        if thing == 4:
                            value *= (1-alpha)**3
                        elif thing == 0 or thing == 6 or thing == 5:
                            value *= alpha * (1-alpha)**2
                        elif thing == 7 or thing == 2 or thing == 1:
                            value *= (alpha**2) * (1-alpha)
                        else:
                            value *= alpha**3
                if output == 5:
                    for thing in [input1, input2]:
                        if thing == 5:
                            value *= (1-alpha)**3
                        elif thing == 7 or thing == 1 or thing == 4:
                            value *= alpha * (1-alpha)**2
                        elif thing == 0 or thing == 6 or thing == 3:
                            value *= (alpha**2) * (1-alpha)
                        else:
                            value *= alpha**3
                if output == 6:
                    for thing in [input1, input2]:
                        if thing == 6:
                            value *= (1-alpha)**3
                        elif thing == 7 or thing == 4 or thing == 2:
                            value *= alpha * (1-alpha)**2
                        elif thing == 0 or thing == 5 or thing == 3:
                            value *= (alpha**2) * (1-alpha)
                        else:
                            value *= alpha**3
                if output == 7:
                    for thing in [input1, input2]:
                        if thing == 7:
                            value *= (1-alpha)**3
                        elif thing == 6 or thing == 5 or thing == 3:
                            value *= alpha * (1-alpha)**2
                        elif thing == 1 or thing == 2 or thing == 4:
                            value *= (alpha**2) * (1-alpha)
                        else:
                            value *= alpha**3
                distribution[output][input1][input2] = value
    return distribution

def show_distribution_matrix2():
    distribution = [[['a','a','a','a'], ['a','a','a','a'], ['a','a','a','a'], ['a','a','a','a']],
                    [['a','a','a','a'], ['a','a','a','a'], ['a','a','a','a'], ['a','a','a','a']],
                    [['a','a','a','a'], ['a','a','a','a'], ['a','a','a','a'], ['a','a','a','a']],
                    [['a','a','a','a'], ['a','a','a','a'], ['a','a','a','a'], ['a','a','a','a']]]
    for output in range(4):
        for input1 in range(4):
            for input2 in range(4):
                value = "1/4"
                if output == 0:
                    for thing in [input1, input2]:
                        if thing == 0:
                            value += "(1-a)^2"
                        elif thing == 1 or thing == 2:
                            value += "a*(1-a)"
                        else:
                            value += "a**2"
                elif output == 1:
                    for thing in [input1, input2]:
                        if thing == 1:
                            value += "(1-a)^2"
                        elif thing == 0 or thing == 3:
                            value += "a*(1-a)"
                        else:
                            value += "a**2"
                elif output == 2:
                    for thing in [input1, input2]:
                        if thing == 2:
                            value += "(1-a)^2"
                        elif thing == 0 or thing == 3:
                            value += "a*(1-a)"
                        else:
                            value += "a**2"
                else:
                    for thing in [input1, input2]:
                        if thing == 3:
                            value += "(1-a)^2"
                        elif thing == 1 or thing == 2:
                            value += "a*(1-a)"
                        else:
                            value += "a**2"
                distribution[output][input1][input2] = value
    return distribution

def distribution_matrix(alpha):
    distribution = np.zeros((2,2,2))
    for output in range(2):
        for input1 in range(2):
            for input2 in range(2):
                value = 1/2
                if output == 0:
                    for thing in [input1, input2]:
                        if thing == 0:
                            value *= (1-alpha)
                        else:
                            value *= alpha
                else:
                    for thing in [input1, input2]:
                        if thing == 1:
                            value *= (1-alpha)
                        else:
                            value *= alpha
                distribution[output][input1][input2] = value
    return distribution

def distribution_matrix_x4(subset):
    distribution = np.zeros((4,2,2))
    for output in range(4):
        for input1 in range(2):
            for input2 in range(2):
                if (output, input1, input2) in subset:
                    distribution[output][input1][input2] = 1/len(subset)
    return distribution

def find_win_prob_x4(f, g, distribution):
    """
    - f is of the form [a0, a1, a2, a3] where ai is the output of player 1 for input i.
    """
    prob = 0
    for output in range(4):
        for input_player1 in range(2):
            for input_player2 in range(2):
                if f[input_player1] == g[input_player2] == output:
                    prob += distribution[output][input_player1][input_player2]
    return prob

def find_max_win_prob_x4(subset):
    max_win_prob = 0
    distribution = distribution_matrix_x4(subset)
    for a1 in range(4):
        for a2 in range(4):
            for b1 in set([a1, a2]):
                for b2 in set([a1, a2]):
                    prob = find_win_prob_x4([a1, a2], [b1, b2], distribution)
                    if prob > max_win_prob:
                        max_win_prob = prob
                        #print([a1, a2, a3, a4], [b1, b2, b3, b4], prob)

    return max_win_prob

def find_win_prob_example2(f, g, distribution):
    """
    - f is of the form [a0, a1, a2, a3] where ai is the output of player 1 for input i.
    """
    prob = 0
    for output in range(4):
        for input_player1 in range(4):
            for input_player2 in range(4):
                if f[input_player1] == g[input_player2] == output:
                    prob += distribution[output][input_player1][input_player2]
    return prob

def find_win_prob_example1x3(f, g, distribution):
    """
    - f is of the form [a0, a1, a2, a3] where ai is the output of player 1 for input i.
    """
    prob = 0
    for output in range(8):
        for input_player1 in range(8):
            for input_player2 in range(8):
                if f[input_player1] == g[input_player2] == output:
                    prob += distribution[output][input_player1][input_player2]
    return prob

def distribution_matrix_xa3(subset):
    distribution = np.zeros((3,3,2))
    for output in range(4):
        for input1 in range(3):
            for input2 in range(2):
                if (output, input1, input2) in subset:
                    distribution[output][input1][input2] = 1/len(subset)
    return distribution

def find_win_prob_xa3(f, g, distribution):
    """
    - f is of the form [a0, a1, a2, a3] where ai is the output of player 1 for input i.
    """
    prob = 0
    for output in range(3):
        for input_player1 in range(3):
            for input_player2 in range(2):
                if f[input_player1] == g[input_player2] == output:
                    prob += distribution[output][input_player1][input_player2]
    return prob

def find_max_win_prob_xa3(subset):
    max_win_prob = 0
    distribution = distribution_matrix_xa3(subset)
    for a1 in range(3):
        for a2 in range(3):
            for a3 in range(3):
                for b1 in set([a1, a2, a3]):
                    for b2 in set([a1, a2, a3]):
                        prob = find_win_prob_xa3([a1, a2, a3], [b1, b2], distribution)
                        if prob > max_win_prob:
                            max_win_prob = prob
                            #print([a1, a2, a3, a4], [b1, b2, b3, b4], prob)

    return max_win_prob

def find_max_win_prob_example2(alpha):
    max_win_prob = 0
    distribution = distribution_matrix2(alpha)
    for a1 in range(4):
        for a2 in range(4):
            for a3 in range(4):
                for a4 in range(4):
                    for b1 in set([a1, a2, a3, a4]):
                        for b2 in set([a1, a2, a3, a4]):
                            for b3 in set([a1, a2, a3, a4]):
                                for b4 in set([a1, a2, a3, a4]):

                                    prob = find_win_prob_example2([a1, a2, a3, a4], [b1, b2, b3, b4], distribution)
                                    if prob > max_win_prob:
                                        max_win_prob = prob
                                        #print([a1, a2, a3, a4], [b1, b2, b3, b4], prob)

    return max_win_prob


def find_max_win_prob_example1x3(alpha):
    max_win_prob = 0
    distribution = distribution_matrix3(alpha)
    for a1 in range(8):
        for a2 in range(8):
            for a3 in range(8):
                for a4 in range(8):
                    for a5 in range(8):
                        for a6 in range(8):
                            for a7 in range(8):
                                for a8 in range(8):
                                    for b1 in set([a1, a2, a3, a4, a5, a6, a7, a8]):
                                        for b2 in set([a1, a2, a3, a4, a5, a6, a7, a8]):
                                            for b3 in set([a1, a2, a3, a4, a5, a6, a7, a8]):
                                                for b4 in set([a1, a2, a3, a4, a5, a6, a7, a8]):
                                                    for b5 in set([a1, a2, a3, a4, a5, a6, a7, a8]):
                                                        for b6 in set([a1, a2, a3, a4, a5, a6, a7, a8]):
                                                            for b7 in set([a1, a2, a3, a4, a5, a6, a7, a8]):
                                                                for b8 in set([a1, a2, a3, a4, a5, a6, a7, a8]):

                                                                    prob = find_win_prob_example1x3([a1, a2, a3, a4, a5, a6, a7, a8], [b1, b2, b3, b4, b5, b6, b7, b8], distribution)
                                                                    if prob > max_win_prob:
                                                                        max_win_prob = prob
                                                                        print([a1, a2, a3, a4, a5, a6, a7, a8], [b1, b2, b3, b4, b5, b6, b7, b8], prob)

    return max_win_prob

def find_max_win_prob_example1x3_attempt2(alpha):
    max_win_prob = 0
    distribution = distribution_matrix3(alpha)
    for a1 in range(8):
        for a2 in range(8):
            for a3 in range(8):
                for a4 in range(8):
                    for a5 in range(8):
                        for a6 in range(8):
                            for a7 in range(8):
                                for a8 in range(8):
                                    prob = find_win_prob_example1x3([a1, a2, a3, a4, a5, a6, a7, a8], [a1, a2, a3, a4, a5, a6, a7, a8], distribution)
                                    if prob > max_win_prob:
                                        max_win_prob = prob
                                        print([a1, a2, a3, a4, a5, a6, a7, a8], prob)

    return max_win_prob

if __name__ == "__main__":
    #alpha = 1 - (1 / sqrt(2))
    alpha = 0.3
    print(find_max_win_prob_example1x3_attempt2(alpha))
    #print(find_max_win_prob_example1x3(alpha))
    #print(find_max_win_prob_x2())
    """
    alphas = np.arange(start=0, stop=0.5, step=0.01)
    probs = []
    for alpha in alphas:
        c = find_max_win_prob_example2(alpha)
        print(alpha, c)
        probs.append(c)

    plt.plot(alphas, probs)
    plt.show()
    """

    """
    strategy = [[[1,1,1,0], [1,1,1,0], [1,1,1,0], [0,0,0,0]],
                [[1,1,0,1], [1,1,0,1], [0,0,0,0], [1,1,0,1]],
                [[1,0,1,1], [0,0,0,0], [1,0,1,1], [1,0,1,1]],
                [[0,0,0,0], [0,1,1,1], [0,1,1,1], [0,1,1,1]]]
    distribution = show_distribution_matrix2()
    ns_win_prob = ''
    for output in range(4):
        for input1 in range(4):
            for input2 in range(4):
                if strategy[output][input1][input2]:
                    ns_win_prob += ("+ " + distribution[output][input1][input2] + " ")
    print(ns_win_prob[2:])
    """

    #print(find_win_prob_example1x3([0,0,0,0,0,0,0,7], [0,0,0,0,0,0,0,7], distribution_matrix3(alpha)))
    #print(find_max_win_prob_example1x3(alpha))