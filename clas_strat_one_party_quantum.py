import numpy as np
import cvxpy as cp
from first_sdp import real_to_complex, complex_to_real, combine

def calc_constant(subset, f, x):
    constant = 0
    # we sum over b in B
    for b in range(2):
        # delta[f(b) = x]
        if f[b] == x:
            # calc P(x,b)
            for element in subset:
                if element[0] == x and element[1] == b:
                    # we assume uniform distribution.
                    constant += 1/len(subset)
    return constant

def SDP(q0, q1, subset, strat_player2):
    As = []
    bs = []

    # constraints on form (result should be 8x8 block matrix with top right and bottom left equal to 0)
    for offset1 in range(2):
        for offset2 in range(2):
            for i in range(2):
                for j in range(2):
                    A = np.zeros((8,8))
                    A[offset1 * 4 + i + 2][offset2 * 4 + j] = 1
                    # This one might be unnecessary but ensures symmetry of A. (to test)
                    A[offset2 * 4 + j][offset1 * 4 + i + 2] = 1
                    As.append(A)
                    bs.append(0)
                    #print(A)

    # POVM constraints.
    for offset1 in range(2):
        for offset2 in range(2):
            for i in range(2):
                for j in range(2):
                    A = np.zeros((8,8))

                    A[offset1*4 + i][offset2*4 + j] = 1
                    A[offset1*4 + i + 2][offset2*4 + j + 2] = 1
                    A[offset1*4 + j][offset1*4 + i] = 1
                    A[offset1*4 + j + 2][offset1*4 + i + 2] = 1
                    As.append(A)

                    if i == j:
                        bs.append(1)
                    else:
                        bs.append(0)


    # TODO: calculate constant sum_{b \in B} P(x,b) delta[f(a) = x]
    c0 = calc_constant(subset, strat_player2, 0)
    c1 = calc_constant(subset, strat_player2, 1)

    # Multiply by 1/2 because we expand the matrix.
    C = combine(1/2 * c0 * q0, 1/2 * c1* q1)
    C = complex_to_real(C)
    #print(C)

    X = cp.Variable((8,8), symmetric=True)
    # The operator >> denotes matrix inequality.
    constraints = [X >> 0]
    constraints += [cp.trace(As[i] @ X) == bs[i] for i in range(len(As))]
    prob = cp.Problem(cp.Maximize(cp.trace(C @ X)), constraints)
    prob.solve()

    #print(X.value)
    complex_X = real_to_complex(X.value)
    # Print result.
    #print("The optimal value is", prob.value)
    #print("A solution X is")
    #print(complex_X)
    return prob.value

def max_class_win_prob(q0, q1, subset):
    max_prob = 0
    for b0 in range(2):
        for b1 in range(2):
            prob = SDP(q0, q1, subset, [b0,b1])
            if prob > max_prob:
                max_prob = prob
    return max_prob

if __name__ == "__main__":
    #print(calc_constant([(0,0), (1,0), (1,0)], [0,0], 1))

    # Should be the same as just trying to discriminate the two given states
    #print(SDP(np.array([[1,0],[0,0]]), np.array([[0.5, 0.5],[0.5, 0.5]]), [(0,0), (1,1)], [0,1]))

    # Should be 0.5 (?)
    #print(SDP(np.array([[1,0],[0,0]]), np.array([[0.5, 0.5],[0.5, 0.5]]), [(0,0), (1,0)], [0,1]))

    print(max_class_win_prob(np.array([[1,0],[0,0]]), np.array([[0.5, 0.5],[0.5, 0.5]]), [(0,0), (1,0)]))