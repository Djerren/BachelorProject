from fractions import Fraction

def is_relevant(strategy):
    for j in range(2**3):
        bitstring = '{0:03b}'.format(j)
        value1 = Fraction(strategy[int('000' + bitstring, 2)])
        value2 = Fraction(strategy[int('111' + bitstring, 2)])
        if value1 > Fraction(1,2) or value2 > Fraction(1,2):
            return True

    return False

def is_deterministic(strategy):
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

def write_to_file(strategy_list, file_name):
    for i in range(len(strategy_list)):
        strategy_list[i] = " ".join(strategy_list[i])
    to_file = "\n".join(strategy_list)
    with open(file_name, 'w') as f:
        f.write(to_file)

def filter_three_players():
    deterministic_strategies = []
    relevant_ns_strategies = []
    with open("three_player_vertices.txt") as strategies:
        for i, line in enumerate(strategies):
            if i >= 3 and line != "end":
                line_split = line[3:len(line) - 1].split(" ")
                if is_relevant(line_split):
                    if is_deterministic(line_split):
                        deterministic_strategies.append(line_split)
                    else:
                        relevant_ns_strategies.append(line_split)
    write_to_file(deterministic_strategies, "three_player_relevant_det_strats.txt")
    write_to_file(relevant_ns_strategies, "three_player_relevant_ns_strats.txt")



if __name__ == "__main__":
    filter_three_players()