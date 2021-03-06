# This function takes a file consisting of the vertices of a no-signalling polytope and filters out
# all the strategies that are useless for LSSD (see lemma 3.1 in overleaf).
#
# Currently only does this for the case of three players where all sets are binary.

from fractions import Fraction

def is_relevant_three_player(strategy):
    """
    This function takes a strategy for the three player LSSD problem with binary inputs and outputs
    and decides if it is useful or not (see lemma 3.1). It is useless if
    the variable corresponding to some bitstring xxxabc is larger than 1/2.
    """
    for j in range(2**3):
        bitstring = '{0:03b}'.format(j)
        value1 = Fraction(strategy[int('000' + bitstring, 2)])
        value2 = Fraction(strategy[int('111' + bitstring, 2)])
        if value1 > Fraction(1,2) or value2 > Fraction(1,2):
            return True

    return False

def is_relevant_two_player_x3(strategy):
    for j in range(4):
        value1 = Fraction(strategy[j])
        value2 = Fraction(strategy[4*4 + j])
        value3 = Fraction(strategy[8*4 + j])
        if value1 > Fraction(1,3) or value2 > Fraction(1,3) or value3 > Fraction(1,3):
            return True

    return False

def is_deterministic_three_player(strategy):
    """
    This function decides whether a strategy for the three player LSSD problem with binary inputs and outputs
    is deterministic. a strategy is deterministic if each Q(x_a|a) is either 0 or 1 (and similar for the other players).
    """

    # In each loop, target is a bitstring representing the possible combinations of input and
    # output for a certain player. We then sum over all possible outputs of the other two players and set there inputs
    # to 0, since it does not matter what their inputs are according to the no-signalling constraints.
    # If we find a value that is not 0 or 1, we return False, otherwise we return True at the very end.
    for j in range(2**2):
        target = '{0:02b}'.format(j)
        conditional_prob = Fraction()
        for k in range(2**2):
            sum_variables = '{0:02b}'.format(k)
            conditional_prob += Fraction(strategy[int(target[0] + sum_variables[0] + sum_variables[1] + target[1] + '00', 2)])

        if conditional_prob != Fraction(0) and conditional_prob != Fraction(1):
            return False

    for j in range(2**2):
        target = '{0:02b}'.format(j)
        conditional_prob = Fraction()
        for k in range(2**2):
            sum_variables = '{0:02b}'.format(k)
            conditional_prob += Fraction(strategy[int(sum_variables[0] + target[0] + sum_variables[1] + '0' + target[1] + '0', 2)])

        if conditional_prob != Fraction(0) and conditional_prob != Fraction(1):
            return False

    for j in range(2**2):
        target = '{0:02b}'.format(j)
        conditional_prob = Fraction()
        for k in range(2**2):
            sum_variables = '{0:02b}'.format(k)
            conditional_prob += Fraction(strategy[int(sum_variables[0] + sum_variables[1] + target[0]+ '00' + target[1], 2)])

        if conditional_prob != Fraction(0) and conditional_prob != Fraction(1):
            return False

    return True

def is_deterministic_two_player_binary(strategy):
    for j in range(2**2):
        target = '{0:02b}'.format(j)
        conditional_prob = Fraction()
        for k in range(2):
            sum_variables = '{0:01b}'.format(k)
            conditional_prob += Fraction(strategy[int(target[0] + sum_variables + target[1] + '0', 2)])

        if conditional_prob != Fraction(0) and conditional_prob != Fraction(1):
            return False

    for j in range(2**2):
        target = '{0:02b}'.format(j)
        conditional_prob = Fraction()
        for k in range(2):
            sum_variables = '{0:01b}'.format(k)
            conditional_prob += Fraction(strategy[int(sum_variables[0] + target[0] + '0' + target[1], 2)])

        if conditional_prob != Fraction(0) and conditional_prob != Fraction(1):
            return False

    return True

def is_deterministic_two_player_x3(strategy):
    for x_a in range(3):
        for a in range(2):
            conditional_prob = Fraction()
            for x_b in range(3):
                conditional_prob += Fraction(strategy[(3*x_a + x_b) * 4 + (2*a)])

            if conditional_prob != Fraction(0) and conditional_prob != Fraction(1):
                return False

    for x_b in range(3):
        for b in range(2):
            conditional_prob = Fraction()
            for x_a in range(3):
                conditional_prob += Fraction(strategy[(3*x_a + x_b) * 4 + b])

            if conditional_prob != Fraction(0) and conditional_prob != Fraction(1):
                return False

    return True

def write_to_file(strategy_list, file_name):
    """
    This function takes a list of strategies and writes them to a file.
    """
    for i in range(len(strategy_list)):
        strategy_list[i] = " ".join(strategy_list[i])
    to_file = "\n".join(strategy_list)
    with open(file_name, 'w') as f:
        f.write(to_file)

def filter_three_players():
    """
    This function loops over all vertices is the no-signalling polytope for three players with binary inputs and outputs
    and determines which of them are relevant for LSSD and sorts the remaining strategies into deterministic and
    non-deterministic strategies.
    """
    deterministic_strategies = []
    relevant_ns_strategies = []
    with open("three_player_vertices.txt") as strategies:
        for i, line in enumerate(strategies):
            if i >= 3 and line != "end":
                line_split = line[3:len(line) - 1].split(" ")
                if is_relevant_three_player(line_split):
                    if is_deterministic_three_player(line_split):
                        deterministic_strategies.append(line_split)
                    else:
                        relevant_ns_strategies.append(line_split)
    write_to_file(deterministic_strategies, "three_player_relevant_det_strats.txt")
    write_to_file(relevant_ns_strategies, "three_player_relevant_ns_strats.txt")

def filter_two_player_binary():
    deterministic_strategies = []
    relevant_ns_strategies = []
    with open("two_player_vertices.txt") as strategies:
        for i, line in enumerate(strategies):
            if i >= 3 and line != "end":
                line_split = line[3:len(line) - 1].split(" ")
                if is_deterministic_two_player_binary(line_split):
                    deterministic_strategies.append(line_split)
                else:
                    relevant_ns_strategies.append(line_split)
    write_to_file(deterministic_strategies, "two_player_binary_det_strats.txt")
    write_to_file(relevant_ns_strategies, "two_player_binary_ns_strats.txt")

def filter_two_player_x3():
    deterministic_strategies = []
    relevant_ns_strategies = []
    with open("two_player_x3_vertices.txt") as strategies:
        for i, line in enumerate(strategies):
            if i >= 3 and line != "end":
                line_split = line[3:len(line) - 1].split(" ")
                if is_relevant_two_player_x3(line_split):
                    if is_deterministic_two_player_x3(line_split):
                        deterministic_strategies.append(line_split)
                    else:
                        relevant_ns_strategies.append(line_split)
    write_to_file(deterministic_strategies, "two_player_x3_det_strats.txt")
    write_to_file(relevant_ns_strategies, "two_player_x3_ns_strats.txt")



if __name__ == "__main__":
    filter_two_player_x3()