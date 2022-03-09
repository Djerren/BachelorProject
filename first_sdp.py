# Import packages.
import cvxpy as cp
import numpy as np


def example():
    # Generate a random SDP.
    n = 3
    p = 3
    np.random.seed(1)
    # This is not symmetric??
    C = np.random.randn(n, n)
    A = []
    b = []
    #print(C)
    for i in range(p):
        A.append(np.random.randn(n, n))
        b.append(np.random.randn())

    # Define and solve the CVXPY problem.
    # Create a symmetric matrix variable.
    X = cp.Variable((n,n), symmetric=True)
    # The operator >> denotes matrix inequality.
    constraints = [X >> 0]
    constraints += [
        cp.trace(A[i] @ X) == b[i] for i in range(p)
    ]
    prob = cp.Problem(cp.Minimize(cp.trace(C @ X)),
                      constraints)
    prob.solve()

    # Print result.
    print("The optimal value is", prob.value)
    print("A solution X is")
    print(X.value)

def complex_to_real(complex_matrix):
    rows, cols = np.shape(complex_matrix)
    real_matrix = [[0.0]*cols*2]
    for i in range(rows):
        new_row = np.append(complex_matrix[i].real, -complex_matrix[i].imag)
        real_matrix = np.append(real_matrix, [new_row], axis=0)
    real_matrix = real_matrix[1:]

    for i in range(rows):
        new_row = np.append(complex_matrix[i].imag, complex_matrix[i].real)
        real_matrix = np.append(real_matrix, [new_row], axis=0)
    return real_matrix

def real_to_complex(real_matrix):
    rows, cols = np.shape(real_matrix)
    complex_matrix = np.zeros((int(rows/2), int(cols/2)), dtype = complex)
    for i in range(int(rows/2)):
        for j in range(int(cols/2)):
            complex_matrix[i][j] = real_matrix[i][j] - real_matrix[i][j + int(cols/2)]*1j
    return complex_matrix

def combine(q1, q2):
    rows, cols = np.shape(q1)
    combined_matrix = [[0.0]*cols*2]
    for i in range(rows):
        new_row = np.append(q1[i], np.zeros(cols))
        combined_matrix = np.append(combined_matrix, [new_row], axis=0)
    combined_matrix = combined_matrix[1:]

    for i in range(rows):
        new_row = np.append(np.zeros(cols), q2[i])
        combined_matrix = np.append(combined_matrix, [new_row], axis=0)
    return combined_matrix

def discriminate_two_states(q1, q2):
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

    """
    for A in As:
        print(A)
    """

    # 1/4 is because each state is chosen with prob 1/2 and because of expanding of matrices we need the other 1/2
    C = combine(1/4 * q1,1/4 * q2)
    C = complex_to_real(C)
    print(C)

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
    print("The optimal value is", prob.value)
    print("A solution X is")
    print(complex_X)


if __name__ == "__main__":
    np.set_printoptions(precision=4, suppress=True)
    #example()

    """
    matrix =np.array([[2,3]])
    print(matrix)
    print(np.append(matrix, [[8,9]], axis=0))
    """

    """
    a = np.array([[1+2j, 3+4j], [3 + 5j, 2 + 8j]])
    print(real_to_complex(complex_to_real(a)))
    """

    discriminate_two_states(np.array([[1,0],[0,0]]),np.array([[0.5,0.5], [0.5,0.5]]))
    #print(complex_to_real(np.array([[1, 2+2j],[2-2j, 3]])))