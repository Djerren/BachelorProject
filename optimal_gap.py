from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, PULP_CBC_CMD
from fractions import Fraction

def two_player_binary_LP_pulp(det_strats, ns_strats, set_to_equality):
    model = LpProblem(name="max_gap_2player_bin", sense=LpMaximize)

    variables = []
    for i in range(2**3):
        variables.append(LpVariable(name='{0:03b}'.format(i), lowBound = 0))

    max_det = LpVariable(name='maxdet', lowBound=0)
    max_ns = LpVariable(name='maxns', lowBound=0)

    model += (sum([variable for variable in variables]) == 1)

    for strategy in det_strats:
        model += (max_det - sum([strategy[int('{0:03b}'.format(i)[0]*2 + '{0:03b}'.format(i)[1] + '{0:03b}'.format(i)[2], 2)] *
                                 variables[int('{0:03b}'.format(i), 2)] for i in range(2**3)]) >= 0)

    for j, strategy in enumerate(ns_strats):
        if j == set_to_equality:
            model += (max_ns - sum([strategy[int('{0:03b}'.format(i)[0]*2 + '{0:03b}'.format(i)[1] + '{0:03b}'.format(i)[2], 2)] *
                                     variables[int('{0:03b}'.format(i), 2)] for i in range(2**3)]) == 0)
        else:
            model += (max_ns - sum([strategy[int('{0:03b}'.format(i)[0]*2 + '{0:03b}'.format(i)[1] + '{0:03b}'.format(i)[2], 2)] *
                                     variables[int('{0:03b}'.format(i), 2)] for i in range(2**3)]) >= 0)

    # This constraint makes sure that whenever deterministic strategies are strictly
    # better that non-deterministic strategies, the LP has no solution.
    # (without this constraint, the solution could be negative). (honestly might be unnecessary)
    model += (max_ns - max_det >= 0)

    obj_func = max_ns - max_det
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

def max_gap_two_player_binary():
    det_strats = read_strategies_from_file("two_player_binary_det_strats.txt")
    ns_strats = read_strategies_from_file("two_player_binary_ns_strats.txt")

    max_gap = 0
    for i in range(len(ns_strats)):
        gap = two_player_binary_LP_pulp(det_strats, ns_strats, i)
        if gap > max_gap:
            max_gap = gap

    return max_gap

def read_strategies_from_file(file):
    strategies = []
    with open(file) as f:
        for line in f:
            strategy = list(map(Fraction, line.split(" ")))
            strategies.append(strategy)

    return strategies

if __name__ == "__main__":
    print(max_gap_two_player_binary())

