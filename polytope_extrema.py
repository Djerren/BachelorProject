# Polytope_extrema.py can find the vertices (extrema) of the non-signalling polytope corresponding to
# a number of players and their question and answer sets. To do this, it makes use of the library pycddlib,
# which works by adding constraints to a matrix. One constraint is one line of a matrix [b  -A] and represents
# A_ix <= b_i. If we mention linear=True when adding a constraint, the constraint will be added as an equality.
#
# Currently there are functions to do this for two and three players, where their question and answer sets are
# all binary.

import cdd

def three_players():
    """
    This function finds the vertices of the extreme points of the no-signalling polytope for three players each
    with binary input and output. It writes the results to a file. This function is very similar to the function in
    no-signalling.py, most importantly: we see each variable as a bitstring of length 6 and reference them by the
    integer value of that bitstring (+1 since the first number in a constraint is the value of b).
    """

    # Firstly, we need that each of the variables is positive, so we add the constraints -x <= 0.
    positivity = []
    for i in range(2**6):
        rule = [0] * (2**6 + 1)

        # this is positive since the matrix [b  -A] will represent Ax <= b
        rule[i+1] = 1
        positivity.append(rule.copy())

    matrix = cdd.Matrix(positivity)

    # Here we add the non signalling constraints: two sums that must be equal, so there difference must be 0.
    nosignalling_constraints = []
    for i in range(2**4):
        bitstring = '{0:04b}'.format(i)
        rule = [0]*(2**6 + 1)
        rule[int('0' + bitstring[0] + bitstring[1] + '0' + bitstring[2] + bitstring[3], 2) + 1] = 1
        rule[int('1' + bitstring[0] + bitstring[1] + '0' + bitstring[2] + bitstring[3], 2) + 1] = 1
        rule[int('0' + bitstring[0] + bitstring[1] + '1' + bitstring[2] + bitstring[3], 2) + 1] = -1
        rule[int('1' + bitstring[0] + bitstring[1] + '1' + bitstring[2] + bitstring[3], 2) + 1] = -1
        nosignalling_constraints.append(rule.copy())

    for i in range(2**4):
        bitstring = '{0:04b}'.format(i)
        rule = [0]*(2**6 + 1)
        rule[int(bitstring[0] + '0' + bitstring[1] + bitstring[2] + '0' + bitstring[3], 2) + 1] = 1
        rule[int(bitstring[0] + '1' + bitstring[1] + bitstring[2] + '0' + bitstring[3], 2) + 1] = 1
        rule[int(bitstring[0] + '0' + bitstring[1] + bitstring[2] + '1' + bitstring[3], 2) + 1] = -1
        rule[int(bitstring[0] + '1' + bitstring[1] + bitstring[2] + '1' + bitstring[3], 2) + 1] = -1
        nosignalling_constraints.append(rule.copy())

    for i in range(2**4):
        bitstring = '{0:04b}'.format(i)
        rule = [0]*(2**6 + 1)
        rule[int(bitstring[0] + bitstring[1] + '0' + bitstring[2] + bitstring[3] + '0', 2) + 1] = 1
        rule[int(bitstring[0] + bitstring[1] + '1' + bitstring[2] + bitstring[3] + '0', 2) + 1] = 1
        rule[int(bitstring[0] + bitstring[1] + '0' + bitstring[2] + bitstring[3] + '1', 2) + 1] = -1
        rule[int(bitstring[0] + bitstring[1] + '1' + bitstring[2] + bitstring[3] + '1', 2) + 1] = -1
        nosignalling_constraints.append(rule.copy())

    # These constraints are equality constraints, so linear = True.
    matrix.extend(nosignalling_constraints, linear = True)

    # We add the the constraints that make sure the values form a conditional distribution.
    distribution_constraints = []
    for i in range(2**3):
        condition = '{0:03b}'.format(i)
        rule = [0] * (2**6 + 1)
        rule[0] = 1
        for j in range(2**3):
            outcome = '{0:03b}'.format(j)

            # Note again the negativity, since [b  -A] represents Ax <= b
            rule[int(outcome + condition, 2) + 1] = -1
        distribution_constraints.append(rule.copy())

    matrix.extend(distribution_constraints, linear = True)

    # We say that the matrix represents a polytope by inequalities (other option is by giving vertices and rays).
    # canonicalize() gets rid of unnecessary constraints.
    matrix.rep_type = cdd.RepType.INEQUALITY
    matrix.canonicalize()

    # The matrix is now interpreted as a polyhedron representation and the othere representation is found and written
    # to a file (so this file contains a list of all the vertices (and rays))
    poly = cdd.Polyhedron(matrix)
    with open('three_player_vertices.txt', 'w') as f:
        f.write(str(poly.get_generators()))

def two_players():
    """
    This function finds the vertices of the extreme points of the no-signalling polytope for three players each
    with binary input and output. It writes the results to a file. It works very similar to three_players().
    """
    positivity = []
    for i in range(2**4):
        rule = [0] * (2**4 + 1)
        rule[i+1] = 1
        positivity.append(rule.copy())

    matrix = cdd.Matrix(positivity)

    nosignalling_constraints = []
    for i in range(2**2):
        bitstring = '{0:02b}'.format(i)
        rule = [0]*(2**4 + 1)
        rule[int('0' + bitstring[0] + '0' + bitstring[1], 2) + 1] = 1
        rule[int('1' + bitstring[0] + '0' + bitstring[1], 2) + 1] = 1
        rule[int('0' + bitstring[0] + '1' + bitstring[1], 2) + 1] = -1
        rule[int('1' + bitstring[0] + '1' + bitstring[1], 2) + 1] = -1
        nosignalling_constraints.append(rule.copy())

    for i in range(2**2):
        bitstring = '{0:02b}'.format(i)
        rule = [0]*(2**4 + 1)
        rule[int(bitstring[0] + '0' + bitstring[1] + '0', 2) + 1] = 1
        rule[int(bitstring[0] + '1' + bitstring[1] + '0', 2) + 1] = 1
        rule[int(bitstring[0] + '0' + bitstring[1] + '1', 2) + 1] = -1
        rule[int(bitstring[0] + '1' + bitstring[1] + '1', 2) + 1] = -1
        nosignalling_constraints.append(rule.copy())

    matrix.extend(nosignalling_constraints, linear = True)

    distribution_constraints = []
    for i in range(2**2):
        condition = '{0:02b}'.format(i)
        rule = [0] * (2**4 + 1)
        rule[0] = 1
        for j in range(2**2):
            outcome = '{0:02b}'.format(j)
            rule[int(outcome + condition, 2) + 1] = -1
        distribution_constraints.append(rule.copy())

    matrix.extend(distribution_constraints, linear = True)
    matrix.rep_type = cdd.RepType.INEQUALITY
    matrix.canonicalize()
    poly = cdd.Polyhedron(matrix)

    with open('two_player_vertices.txt', 'w') as f:
        f.write(str(poly.get_generators()))

if __name__ == "__main__":
    #two_players()
    three_players()