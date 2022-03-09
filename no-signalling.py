# no-signalling.py consists of a function that finds the best winning probability using no-signalling strategies
# for LSSD with three players and |X| = |A| = |B| = |C| = 2.
#
# If this file is run, it compares the winning probability using only classical strategies and using any no-signalling
# strategies of all games where the probability distribution is a uniform distribution over a subset of all possible
# combinations of the 4 values x,a,b and c.

import sys
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, PULP_CBC_CMD
import math
import Classical
import numpy as np
import matplotlib.pyplot as plt

def find_max_win_prob(subset):
    """
    This function finds the best winning probability of a game defined by subset using linear programming.
    """

    # We create the LP problem, which is to maximize the winning probability over all no-signalling strategies.
    model = LpProblem(name="no-signalling_strat", sense=LpMaximize)

    # A no-signalling strategy q is defined by the values of q(x_a, x_b, x_c | a, b, c) for each possible combination of
    # x_a, x_b, x_c, a, b and c. Since these can all only be 0 or 1, we can represent each variable by a bitstring of
    # length 6. So the variable '100110' represents the value of q(1, 0, 0 | 1, 1, 0). Furthermore, each of the
    # variables should be non-negative and we save each variable in a list at the position corresponding to the value
    # of its bitstring representation. So the variable '100110' is stored at position 38 in the list.
    variables = []
    for i in range(2**6):
        variables.append(LpVariable(name='{0:06b}'.format(i), lowBound = 0))

    # In the next three for loops, we add the no-signalling constraints:
    # - q(0, x_b, x_c | 0, b, c) + q(1, x_b, x_c | 0, b, c) = q(0, x_b, x_c | 1, b, c) + q(0, x_b, x_c | 1, b, c)
    #   for each x_b, x_c, b, c.
    # We represent the values x_b, x_c, b, c as a bitstring of length 4 and loop over all possible bitstrings of length
    # 4 to add the given constraint for each possible combination. The other two loops do the same thing, but for the
    # other two parties.
    for i in range(2**4):
        bitstring = '{0:04b}'.format(i)
        model += (variables[int('0' + bitstring[0] + bitstring[1] + '0' + bitstring[2] + bitstring[3], 2)] +
                  variables[int('1' + bitstring[0] + bitstring[1] + '0' + bitstring[2] + bitstring[3], 2)] -
                  variables[int('0' + bitstring[0] + bitstring[1] + '1' + bitstring[2] + bitstring[3], 2)] -
                  variables[int('1' + bitstring[0] + bitstring[1] + '1' + bitstring[2] + bitstring[3], 2)] == 0)

    for i in range(2**4):
        bitstring = '{0:04b}'.format(i)
        model += (variables[int(bitstring[0] + '0' + bitstring[1] + bitstring[2] + '0' + bitstring[3], 2)] +
                  variables[int(bitstring[0] + '1' + bitstring[1] + bitstring[2] + '0' + bitstring[3], 2)] -
                  variables[int(bitstring[0] + '0' + bitstring[1] + bitstring[2] + '1' + bitstring[3], 2)] -
                  variables[int(bitstring[0] + '1' + bitstring[1] + bitstring[2] + '1' + bitstring[3], 2)] == 0)

    for i in range(2**4):
        bitstring = '{0:04b}'.format(i)
        model += (variables[int(bitstring[0] + bitstring[1] + '0' + bitstring[2] + bitstring[3] + '0', 2)] +
                  variables[int(bitstring[0] + bitstring[1] + '1' + bitstring[2] + bitstring[3] + '0', 2)] -
                  variables[int(bitstring[0] + bitstring[1] + '0' + bitstring[2] + bitstring[3] + '1', 2)] -
                  variables[int(bitstring[0] + bitstring[1] + '1' + bitstring[2] + bitstring[3] + '1', 2)] == 0)

    # In this loop we add the constraints that make sure the strategies are well-defined conditional probability
    # functions:
    # - sum_{x_a, x_b, x_c} q(x_a, x_b, x_c | a, b, c) = 1 for all a, b, c.
    # Again, we represent the values for a,b,c as a bitstring an loop over all possible bitstrings. We do something
    # similar to represent the sum.
    for i in range(2**3):
        bitstring = '{0:03b}'.format(i)
        model += (sum([variables[int('{0:03b}'.format(j) + bitstring, 2)] for j in range(2**3)]) == 1)

    # Here we define the objective function:
    # - sum_{x, a, b, c} P(x, a, b, c) * q(x, x, x | a, b, c)
    # Because we are only interested in games where the distribution is uniform over a subset of combinations,
    # P(x,a,b,c) is a constant 1/(nr of combinations in subset).
    multiplier = 1/len(subset)
    obj_func = sum([multiplier * variables[int(3*str(comb[0]) + str(comb[1]) + str(comb[2]) + str(comb[3]), 2)] for comb in subset])
    model += obj_func

    #print(model)

    model.solve(PULP_CBC_CMD(msg=0))

    """
    print(f"status: {model.status}, {LpStatus[model.status]}")

    print(f"objective: {model.objective.value()}")
    for var in model.variables():
        print(f"{var.name}: {var.value()}")
    """

    return model.objective.value()

def three_player():
    # this is a set containing all possible values of (x, a, b, c).
    possible_combinations = [(0,0,0,0), (0,0,0,1), (0,0,1,0), (0,0,1,1),
                             (0,1,0,0), (0,1,0,1), (0,1,1,0), (0,1,1,1),
                             (1,0,0,0), (1,0,0,1), (1,0,1,0), (1,0,1,1),
                             (1,1,0,0), (1,1,0,1), (1,1,1,0), (1,1,1,1)]

    #find_max_win_prob([(0, 1, 1, 0),(1, 1, 1, 1)])

    # We represent a subset by a binary string of length 16, where each bit tells us whether a certain combination
    # is included in the subset or not.
    for i in range(1, 2**16):
        subset_string = '{0:016b}'.format(i)

        subset = []
        for j in range(16):
            if subset_string[j] == '1':
                subset.append(possible_combinations[j])

        # We find the best winning probabilities using only deterministic strategies and
        # using any no-signalling strategy.
        prob1 = find_max_win_prob(subset)
        prob2 = Classical.find_optimal_strategy(subset)

        #print(prob1, prob2)

        # We are interested in those cases where the probabilities differ from eachother.
        if not math.isclose(prob1, prob2):
            print(prob1, prob2, subset)


def find_max_win_prob_example1(alpha):
    distribution = Classical.distribution_matrix2(alpha)

    model = LpProblem(name="no-signalling_strat", sense=LpMaximize)

    variables = []
    for output1 in range(4):
        for output2 in range(4):
            for input1 in range(4):
                for input2 in range(4):
                    variables.append(LpVariable(name=f"{output1}{output2}|{input1}{input2}", lowBound = 0))

    for output2 in range(4):
        for input2 in range(4):
            for input1 in [1,2,3]:
                model += (sum([variables[output1*64 + output2*16 + input2] for output1 in range(4)]) -
                          sum([variables[output1*64 + output2*16 + input1*4 + input2] for output1 in range(4)]) == 0)

    for output1 in range(4):
        for input1 in range(4):
            for input2 in [1,2,3]:
                model += (sum([variables[output1*64 + output2*16 + input1*4] for output2 in range(4)]) -
                          sum([variables[output1*64 + output2*16 + input1*4 + input2] for output2 in range(4)]) == 0)

    for input1 in range(4):
        for input2 in range(4):
            model += (sum([variables[output1*64 + output2*16 + input1*4 + input2] for output1 in range(4) for output2 in range(4)]) == 1)

    obj_func = sum([distribution[output][input1][input2]*variables[output*64 + output*16 + input1*4 + input2] for output in range(4) for input1 in range(4) for input2 in range(4)])
    model += obj_func
    #print(model)

    model.solve(PULP_CBC_CMD(msg=0))
    """
    for var in model.variables():
        print(f"{var.name}: {var.value()}")
    """
    return model.objective.value()

def find_max_win_prob_example1x3(alpha, show=False, show_image=False):
    distribution = Classical.distribution_matrix3(alpha)

    model = LpProblem(name="no-signalling_strat", sense=LpMaximize)

    variables = []
    for output1 in range(8):
        for output2 in range(8):
            for input1 in range(8):
                for input2 in range(8):
                    variables.append(LpVariable(name=f"{output1}{output2}|{input1}{input2}", lowBound = 0))

    for output2 in range(8):
        for input2 in range(8):
            for input1 in [1,2,3,4,5,6,7]:
                model += (sum([variables[output1*512 + output2*64 + input2] for output1 in range(8)]) -
                          sum([variables[output1*512 + output2*64 + input1*8 + input2] for output1 in range(8)]) == 0)

    for output1 in range(8):
        for input1 in range(8):
            for input2 in [1,2,3,4,5,6,7]:
                model += (sum([variables[output1*512 + output2*64 + input1*8] for output2 in range(8)]) -
                          sum([variables[output1*512 + output2*64 + input1*8 + input2] for output2 in range(8)]) == 0)

    for input1 in range(8):
        for input2 in range(8):
            model += (sum([variables[output1*512 + output2*64 + input1*8 + input2] for output1 in range(8) for output2 in range(8)]) == 1)

    obj_func = sum([distribution[output][input1][input2]*variables[output*512 + output*64 + input1*8 + input2] for output in range(8) for input1 in range(8) for input2 in range(8)])
    model += obj_func
    #print(model)

    model.solve(PULP_CBC_CMD(msg=0))

    if show:
        for var in model.variables():
            print(f"{var.name}: {var.value()}")
    if show_image:
        new_array = np.zeros((64, 64))
        for inputs in range(64):
            for outputs in range(64):
                new_array[inputs][outputs] = variables[outputs*64 + inputs].value()

        with open('3_game_ns_strat3.txt', 'w') as f:
            text = ""
            for row in new_array:
                line = ""
                for element in row:
                    line += str(element) + " "
                text += line + "\n"
            f.write(text)


        for line in new_array:
            print(line)
        plt.imshow(np.transpose(new_array), interpolation="none")
        plt.show()

    return model.objective.value()

def find_max_win_prob_x4(subset):
    distribution = Classical.distribution_matrix_x4(subset)

    model = LpProblem(name="no-signalling_strat", sense=LpMaximize)

    variables = []
    for output1 in range(4):
        for output2 in range(4):
            for input1 in range(2):
                for input2 in range(2):
                    variables.append(LpVariable(name=f"{output1}{output2}|{input1}{input2}", lowBound = 0))

    for output2 in range(4):
        for input2 in range(2):
            model += (sum([variables[output1*16 + output2*4 + input2] for output1 in range(4)]) -
                      sum([variables[output1*16 + output2*4 + 2 + input2] for output1 in range(4)]) == 0)

    for output1 in range(4):
        for input1 in range(2):
            model += (sum([variables[output1*16 + output2*4 + input1*2] for output2 in range(4)]) -
                      sum([variables[output1*16 + output2*4 + input1*2 + 1] for output2 in range(4)]) == 0)

    for input1 in range(2):
        for input2 in range(2):
            model += (sum([variables[output1*16 + output2*4 + input1*2 + input2] for output1 in range(4) for output2 in range(4)]) == 1)

    obj_func = sum([distribution[output][input1][input2]*variables[output*16 + output*4 + input1*2 + input2] for output in range(4) for input1 in range(2) for input2 in range(2)])
    model += obj_func
    #print(model)

    model.solve(PULP_CBC_CMD(msg=0))
    """
    for var in model.variables():
        print(f"{var.name}: {var.value()}")
    """
    return model.objective.value()

def find_max_gap_x4():
    possible_combinations = [(0,0,0), (0,0,1), (0,1,0), (0,1,1),
                             (1,0,0), (1,0,1), (1,1,0), (1,1,1),
                             (2,0,0), (2,0,1), (2,1,0), (2,1,1),
                             (3,0,0), (3,0,1), (3,1,0), (3,1,1)]

    for i in range(1, 2**16):
        subset_string = '{0:016b}'.format(i)

        subset = []
        for j in range(16):
            if subset_string[j] == '1':
                subset.append(possible_combinations[j])

        # We find the best winning probabilities using only deterministic strategies and
        # using any no-signalling strategy.
        ns = find_max_win_prob_x4(subset)
        c = Classical.find_max_win_prob_x4(subset)

        #print(prob1, prob2)

        # We are interested in those cases where the probabilities differ from eachother.
        if not math.isclose(ns, c):
            print(ns, c, ns-c, subset)

def find_max_win_prob_xa3(subset):
    distribution = Classical.distribution_matrix_xa3(subset)

    model = LpProblem(name="no-signalling_strat", sense=LpMaximize)

    variables = []
    for output1 in range(3):
        for output2 in range(3):
            for input1 in range(3):
                for input2 in range(2):
                    variables.append(LpVariable(name=f"{output1}{output2}|{input1}{input2}", lowBound = 0))

    for output2 in range(3):
        for input2 in range(2):
            for input1 in [1,2]:
                model += (sum([variables[output1*18 + output2*6 + input2] for output1 in range(3)]) -
                          sum([variables[output1*18 + output2*6 + input1*2 + input2] for output1 in range(3)]) == 0)

    for output1 in range(3):
        for input1 in range(3):
            model += (sum([variables[output1*18 + output2*6 + input1*2] for output2 in range(3)]) -
                      sum([variables[output1*18 + output2*6 + input1*2 + 1] for output2 in range(3)]) == 0)

    for input1 in range(3):
        for input2 in range(2):
            model += (sum([variables[output1*18 + output2*6 + input1*2 + input2] for output1 in range(3) for output2 in range(3)]) == 1)

    obj_func = sum([distribution[output][input1][input2]*variables[output*18 + output*6 + input1*2 + input2] for output in range(3) for input1 in range(3) for input2 in range(2)])
    model += obj_func
    #print(model)

    model.solve(PULP_CBC_CMD(msg=0))
    """
    for var in model.variables():
        print(f"{var.name}: {var.value()}")
    """
    return model.objective.value()

def find_max_gap_xa3():
    possible_combinations = [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (0,2,0), (0,2,1),
                             (1,0,0), (1,0,1), (1,1,0), (1,1,1), (1,2,0), (1,2,1),
                             (2,0,0), (2,0,1), (2,1,0), (2,1,1), (2,2,0), (2,2,1)]

    for i in range(1, 2**18):
        subset_string = '{0:018b}'.format(i)

        subset = []
        for j in range(18):
            if subset_string[j] == '1':
                subset.append(possible_combinations[j])

        # We find the best winning probabilities using only deterministic strategies and
        # using any no-signalling strategy.
        ns = find_max_win_prob_xa3(subset)
        c = Classical.find_max_win_prob_xa3(subset)

        #print(prob1, prob2)

        # We are interested in those cases where the probabilities differ from eachother.
        if not math.isclose(ns, c):
            print(ns, c, ns-c, subset)

if __name__ == "__main__":
    np.set_printoptions(threshold=sys.maxsize)
    """
    alphas = np.arange(start=0, stop=0.5, step=0.01)
    probs1 = []
    probs2 = []
    for alpha in alphas:
        ns = find_max_win_prob_example1(alpha)
        c = Classical.find_max_win_prob_example2(alpha)
        print(alpha)
        probs1.append(c)
        probs2.append(ns)

    plt.plot(alphas, probs1)
    plt.plot(alphas, probs2)
    plt.show()
    """
    """
    alphas = np.arange(start=0.32, stop=0.34, step=0.0005)
    #probs1 = []
    probs2 = []
    for alpha in alphas:
        ns = find_max_win_prob_example1x3(alpha)
        #c = Classical.find_max_win_prob_example2(alpha)
        print(alpha)Two
        #probs1.append(c)
        probs2.append(ns)

    #plt.plot(alphas, probs1)
    plt.plot(alphas, probs2)
    plt.show()
    """

    """
    #alpha = 1 - (1 / math.sqrt(2))
    alpha = 0.37
    #c = Classical.find_max_win_prob_example2(alpha)
    ns = find_max_win_prob_example1(alpha)
    print(ns)
    """
    """
    #alpha = 1 - (1 / math.sqrt(2))
    alpha = 0.33
    ns = find_max_win_prob_example1x3(alpha, False, True)
    print(ns)
    """
    #"""
    alphas = np.arange(start=0, stop=0.5, step=0.005)
    probs1 = []
    probs2 = []
    for alpha in alphas:
        c = Classical.find_max_win_prob_example2(alpha)
        ns = find_max_win_prob_example1(alpha)
        probs1.append(c)
        probs2.append(ns)
        print(alpha)
    plt.plot(alphas, probs1, color='r')
    plt.plot(alphas, probs2, color='b')


    plt.show()
    #"""



    """
    zero = [(0,0,0), (0,0,1), (0,1,0), (0,1,1)]
    one = [(1,0,0), (1,0,1), (1,1,0), (1,1,1)]
    two = [(2,0,0), (2,0,1), (2,1,0), (2,1,1)]
    three = [(3,0,0), (3,0,1), (3,1,0), (3,1,1)]
    subset = [zero[0], zero[1], one[2], one[3], two[0], two[1], two[2], three[1], three[2], three[3]]
    c = Classical.find_max_win_prob_x4(subset)
    ns = find_max_win_prob_x4(subset)
    print(ns-c)

    find_max_gap_xa3()
    """

