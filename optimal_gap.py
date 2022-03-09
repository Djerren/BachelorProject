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

def three_player_binary_LP_pulp(det_strats, ns_strats, set_to_equality):
    model = LpProblem(name="max_gap_2player_bin", sense=LpMaximize)

    variables = []
    for i in range(2**4):
        variables.append(LpVariable(name='{0:03b}'.format(i), lowBound = 0))

    max_det = LpVariable(name='maxdet', lowBound=0)
    max_ns = LpVariable(name='maxns', lowBound=0)

    model += (sum([variable for variable in variables]) == 1)

    for strategy in det_strats:
        model += (max_det - sum([strategy[int('{0:04b}'.format(i)[0]*3 +
                                              '{0:04b}'.format(i)[1] +
                                              '{0:04b}'.format(i)[2] +
                                              '{0:04b}'.format(i)[3], 2)] *
                                 variables[int('{0:04b}'.format(i), 2)] for i in range(2**4)]) >= 0)

    for j, strategy in enumerate(ns_strats):
        if j == set_to_equality:
            model += (max_ns - sum([strategy[int('{0:04b}'.format(i)[0]*3 +
                                                 '{0:04b}'.format(i)[1] +
                                                 '{0:04b}'.format(i)[2] +
                                                 '{0:04b}'.format(i)[3], 2)] *
                                    variables[int('{0:04b}'.format(i), 2)] for i in range(2**4)]) == 0)
        else:
            model += (max_ns - sum([strategy[int('{0:04b}'.format(i)[0]*3 +
                                                 '{0:04b}'.format(i)[1] +
                                                 '{0:04b}'.format(i)[2] +
                                                 '{0:04b}'.format(i)[3], 2)] *
                                    variables[int('{0:04b}'.format(i), 2)] for i in range(2**4)]) >= 0)

    # This constraint makes sure that whenever deterministic strategies are strictly
    # better that non-deterministic strategies, the LP has no solution.
    # (without this constraint, the solution could be negative). (honestly might be unnecessary)
    model += (max_ns - max_det >= 0)

    obj_func = max_ns - max_det
    model += obj_func
    #print(model)

    model.solve(PULP_CBC_CMD(msg=0))

    """
    print(f"status: {model.status}, {LpStatus[model.status]}, gap: {model.objective.value()}")
    print(f"objective: {model.objective.value()}")
    for var in model.variables():
        print(f"{var.name}: {var.value()}")
    """

    return model.objective.value()

def two_player_x3_LP_pulp(det_strats, ns_strats, set_to_equality, show=False, count=0, maximize="gap", ratio_value = 0.5/0.4, bias_value = 0.5/0.2):
    model = LpProblem(name="max_gap_2player_bin", sense=LpMaximize)

    # the variables are named as follows: the variable corresponding to P(x,a,b)
    # is named "xc" where c is the number between 0 and 3 corresponding to the bitstring ab.
    variables = []
    for x in range(3):
        for ab in range(4):
            variables.append(LpVariable(name=str(x)+str(ab), lowBound = 0))

    # We have extra variables for the max win probability for deterministic and
    # non-deterministic strategies.
    max_det = LpVariable(name='maxdet', lowBound=0)
    max_ns = LpVariable(name='maxns', lowBound=0)

    # The sum of all variables (excluding max_det and max_ns) should be 1, such that
    # it is a distribution.
    model += (sum([variable for variable in variables]) == 1)

    # The winning probability of one strategy is given by
    #     sum_{x,a,b} P(x,a,b) Q(x,x | a,b)
    # This also means we only need to look at values of the strategy corresponding
    # to Q(xx|ab) for some x,a,b (so where outputs are the same.)
    for strategy in det_strats:
        model += (max_det - sum([strategy[(16*x + ab)] * variables[4*x + ab]
                                 for x in range(3) for ab in range(4)]) >= 0)

    for j, strategy in enumerate(ns_strats):
        if j == set_to_equality:
            model += (max_ns - sum([strategy[(16*x + ab)] * variables[4*x + ab]
                                     for x in range(3) for ab in range(4)]) == 0)
        else:
            model += (max_ns - sum([strategy[(16*x + ab)] * variables[4*x + ab]
                                    for x in range(3) for ab in range(4)]) >= 0)

    # This constraint makes sure that whenever deterministic strategies are strictly
    # better that non-deterministic strategies, the LP has no solution.
    # (without this constraint, the solution could be negative). (honestly might be unnecessary)
    if maximize == "gap":
        model += (max_ns - max_det >= 0)
    elif maximize == "ratio":
        model += (max_ns - ratio_value * max_det >= 0)
    elif maximize == "bias":
        model += (3*max_ns - (bias_value * 3)*max_det + (bias_value - 1)>=0)

    # objective function is not important for maximize="ratio", since we are only interested in whether there is a solution.
    obj_func = max_ns - max_det
    model += obj_func

    #print(model)

    model.solve(PULP_CBC_CMD(msg=0))

    #print(f"status: {model.status}, {LpStatus[model.status]}, gap: {model.objective.value()}")
    """
    print(f"objective: {model.objective.value()}")
    for var in model.variables():
        print(f"{var.name}: {var.value()}")
    """
    if model.status == 1:
        if show and model.objective.value() > 0:
            if maximize == "gap":
                print(f"status: {model.status}, {LpStatus[model.status]}, gap: {model.objective.value()}")
                print(f"objective: {model.objective.value()}")
                print("distribution:")
                for var in model.variables():
                    print(f"{var.name}: {var.value()},", end=" ")
                strategy = ns_strats[set_to_equality]
                print()
                print("strategy:")
                for x in range(3):
                    for ab in range(4):
                        print(f"{x}{ab}: {strategy[x*16 + ab]},", end=" ")
                print(f"\nstrategy number: {set_to_equality}")
                print("")
                count += 1
            elif maximize == "ratio":
                print(f"solution found:")
                for var in model.variables():
                    print(f"{var.name}: {var.value()},", end=" ")
                print("\n")
            elif maximize == "bias":
                print(f"solution found:")
                for var in model.variables():
                    print(f"{var.name}: {var.value()},", end=" ")
                print("\n")
        return model.objective.value(), count
    else:
        return 0, count

def max_gap_two_player_binary():
    det_strats = read_strategies_from_file("two_player_binary_det_strats.txt")
    ns_strats = read_strategies_from_file("two_player_binary_ns_strats.txt")

    max_gap = 0
    for i in range(len(ns_strats)):
        gap = two_player_binary_LP_pulp(det_strats, ns_strats, i)
        if gap > max_gap:
            max_gap = gap

    return max_gap

def max_gap_three_player_binary():
    det_strats = read_strategies_from_file("three_player_relevant_det_strats.txt")
    ns_strats = read_strategies_from_file("three_player_relevant_ns_strats.txt")

    max_gap = 0
    for i in range(len(ns_strats)):
        gap = three_player_binary_LP_pulp(det_strats, ns_strats, i)
        if gap > max_gap:
            max_gap = gap

    return max_gap

def max_gap_two_player_x3():
    det_strats = read_strategies_from_file("two_player_x3_det_strats.txt")
    ns_strats = read_strategies_from_file("two_player_x3_ns_strats.txt")
    gap_strategies = [2, 12, 34, 36, 41, 45, 133, 135, 137, 139, 279, 289, 303, 308, 319, 323, 328, 329, 334, 335, 463, 474, 497, 517]
    max_gap = 0
    count = 0
    for i in gap_strategies:
        gap, count = two_player_x3_LP_pulp(det_strats, ns_strats, i, True, count, "bias", bias_value=(0.5/0.2)*(100))
        if gap > max_gap:
            max_gap = gap

    return max_gap, count

def read_strategies_from_file(file):
    strategies = []
    with open(file) as f:
        for line in f:
            strategy = list(map(Fraction, line.split(" ")))
            strategies.append(strategy)

    return strategies

if __name__ == "__main__":
    print(f"\n largest gap found: {max_gap_two_player_x3()}")

