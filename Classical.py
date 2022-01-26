# Classical.py consists of all the necessary function to calculate the probability of the best
# classical strategy for LSSD with three parties and |X| = |A| = |B| = |C|.

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
