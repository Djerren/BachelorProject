from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, PULP_CBC_CMD
import math
import Classical

def find_max_win_prob(subset):
    model = LpProblem(name="no-signalling_strat", sense=LpMaximize)

    variables = []
    for i in range(2**6):
        variables.append(LpVariable(name='{0:06b}'.format(i), lowBound = 0))

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

    for i in range(2**3):
        bitstring = '{0:03b}'.format(i)
        model += (sum([variables[int('{0:03b}'.format(j) + bitstring, 2)] for j in range(2**3)]) == 1)

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


if __name__ == "__main__":
    possible_combinations = [(0,0,0,0), (0,0,0,1), (0,0,1,0), (0,0,1,1),
                             (0,1,0,0), (0,1,0,1), (0,1,1,0), (0,1,1,1),
                             (1,0,0,0), (1,0,0,1), (1,0,1,0), (1,0,1,1),
                             (1,1,0,0), (1,1,0,1), (1,1,1,0), (1,1,1,1)]

    #find_max_win_prob([(0, 1, 1, 0),(1, 1, 1, 1)])

    for i in range(1, 2**16):
        subset_string = '{0:016b}'.format(i)

        subset = []
        for j in range(16):
            if subset_string[j] == '1':
                subset.append(possible_combinations[j])
        prob1 = find_max_win_prob(subset)
        prob2 = Classical.find_optimal_strategy(subset)

        #print(prob1, prob2)

        if not math.isclose(prob1, prob2):
            print(prob1, prob2, subset)



