# for converting to binary string: '{0:07b}'.format(12)

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
    This function returns the winning probability of a strategy given by 3 binary functions
    given a subset of tuples (or lists) of 4 bits. (uniform distribution on subset is assumed.)
    """
    win_prob = 0
    for element in subset:
        if element[0] == f(element[1]) == g(element[2]) == h(element[3]):
            win_prob += 1

    # Division does not necessarily need to happen here.
    return win_prob/len(subset)



def find_optimal_strategy(subset):
    max_win_prob = 0
    bin_funcs = [id_func, not_func, bot, top]
    for f in bin_funcs:
        for g in bin_funcs:
            for h in bin_funcs:
                win_prob = find_win_prob(f,g,h, subset)

                # Currently working with floats, should not cause problems.
                # Possible to switch to ints and do division at the end.
                if win_prob > max_win_prob:
                    max_win_prob = win_prob
    return max_win_prob


if __name__ == "__main__":
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
