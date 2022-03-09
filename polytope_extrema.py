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

def two_players_x3():
    """
    This function finds the vertices of the extreme points of the no-signalling polytope for three players each
    with binary input but |X| = 3. It writes the results to a file. It works very similar to three_players(). ordering
    of the variables becomes a bit more of a hassle.
    """

    # each variable q(x_a, x_b | a, b) is at place (3x_a + x_b) * 4 + (2a + b) + 1 in the list... so there are 9*4
    # variables in the list and one more value for b of [b  -A].
    positivity = []
    for i in range(9*4):
        rule = [0] * (9*4 + 1)
        rule[i+1] = 1
        positivity.append(rule.copy())

    matrix = cdd.Matrix(positivity)

    nosignalling_constraints = []
    for x_b in range(3):
        for b in range(2):
            rule = [0]*(9*4 + 1)
            rule[x_b       * 4 + b       + 1] = 1
            rule[(3 + x_b) * 4 + b       + 1] = 1
            rule[(6 + x_b) * 4 + b       + 1] = 1
            rule[x_b       * 4 + (2 + b) + 1] = -1
            rule[(3 + x_b) * 4 + (2 + b) + 1] = -1
            rule[(6 + x_b) * 4 + (2 + b) + 1] = -1
            nosignalling_constraints.append(rule.copy())

    for x_a in range(3):
        for a in range(2):
            rule = [0]*(9*4 + 1)
            rule[(3 * x_a)     * 4 + (2*a)     + 1] = 1
            rule[(3 * x_a + 1) * 4 + (2*a)     + 1] = 1
            rule[(3 * x_a + 2) * 4 + (2*a)     + 1] = 1
            rule[(3 * x_a)     * 4 + (2*a + 1) + 1] = -1
            rule[(3 * x_a + 1) * 4 + (2*a + 1) + 1] = -1
            rule[(3 * x_a + 2) * 4 + (2*a + 1) + 1] = -1
            nosignalling_constraints.append(rule.copy())

    matrix.extend(nosignalling_constraints, linear = True)

    distribution_constraints = []
    for i in range(4):
        rule = [0] * (9*4 + 1)
        rule[0] = 1
        for j in range(9):
            rule[j*4 + i + 1] = -1
        distribution_constraints.append(rule.copy())

    matrix.extend(distribution_constraints, linear = True)

    matrix.rep_type = cdd.RepType.INEQUALITY
    matrix.canonicalize()
    poly = cdd.Polyhedron(matrix)

    with open('two_player_x3_vertices.txt', 'w') as f:
        f.write(str(poly.get_generators()))

def two_players_a3():
    """
    This function finds the vertices of the extreme points of the no-signalling polytope for three players each
    with binary input but |A| = 3. It writes the results to a file. It works very similar to three_players(). ordering
    of the variables becomes a bit more of a hassle.
    """

    # each variable q(x_a, x_b | a, b) is at place 12x_a + 6x_b + 2a + b in the list... so there are 9*4
    # variables in the list and one more value for b of [b  -A].
    positivity = []
    for i in range(2*2*3*2):
        rule = [0] * (2*2*3*2 + 1)
        rule[i+1] = 1
        positivity.append(rule.copy())

    matrix = cdd.Matrix(positivity)

    nosignalling_constraints = []
    for x_b in range(2):
        for b in range(2):
            rule = [0]*(2*2*3*2 + 1)
            rule[     6*x_b +     b + 1] = 1
            rule[12 + 6*x_b +     b + 1] = 1
            rule[     6*x_b + 2 + b + 1] = -1
            rule[12 + 6*x_b + 2 + b + 1] = -1
            nosignalling_constraints.append(rule.copy())

            rule = [0]*(2*2*3*2 + 1)
            rule[     6*x_b + 2   + b + 1] = 1
            rule[12 + 6*x_b + 2   + b + 1] = 1
            rule[     6*x_b + 2*2 + b + 1] = -1
            rule[12 + 6*x_b + 2*2 + b + 1] = -1
            nosignalling_constraints.append(rule.copy())

    for x_a in range(2):
        for a in range(3):
            rule = [0]*(2*2*3*2 + 1)
            rule[12*x_a +     2*a +     1] = 1
            rule[12*x_a + 6 + 2*a +     1] = 1
            rule[12*x_a +     2*a + 1 + 1] = -1
            rule[12*x_a + 6 + 2*a + 1 + 1] = -1
            nosignalling_constraints.append(rule.copy())

    matrix.extend(nosignalling_constraints, linear = True)

    distribution_constraints = []
    for i in range(6):
        rule = [0] * (2*2*3*2 + 1)
        rule[0] = 1
        for j in range(4):
            rule[j*6 + i + 1] = -1
        distribution_constraints.append(rule.copy())

    matrix.extend(distribution_constraints, linear = True)

    matrix.rep_type = cdd.RepType.INEQUALITY
    matrix.canonicalize()
    poly = cdd.Polyhedron(matrix)

    with open('two_player_a3_vertices.txt', 'w') as f:
        f.write(str(poly.get_generators()))

def two_players_ab3():
    """
    This function finds the vertices of the extreme points of the no-signalling polytope for three players each
    with binary input but |A| = 3. It writes the results to a file. It works very similar to three_players(). ordering
    of the variables becomes a bit more of a hassle.
    """

    # each variable q(x_a, x_b | a, b) is at place 18x_a + 9x_b + 3a + b in the list... so there are 9*4
    # variables in the list and one more value for b of [b  -A].
    positivity = []
    for i in range(2*2*3*3):
        rule = [0] * (2*2*3*3 + 1)
        rule[i+1] = 1
        positivity.append(rule.copy())

    matrix = cdd.Matrix(positivity)

    nosignalling_constraints = []
    for x_b in range(2):
        for b in range(3):
            rule = [0]*(2*2*3*3 + 1)
            rule[     9*x_b +     b + 1] = 1
            rule[18 + 9*x_b +     b + 1] = 1
            rule[     9*x_b + 3 + b + 1] = -1
            rule[18 + 9*x_b + 3 + b + 1] = -1
            nosignalling_constraints.append(rule.copy())

            rule = [0]*(2*2*3*3 + 1)
            rule[     9*x_b + 3   + b + 1] = 1
            rule[18 + 9*x_b + 3   + b + 1] = 1
            rule[     9*x_b + 3*2 + b + 1] = -1
            rule[18 + 9*x_b + 3*2 + b + 1] = -1
            nosignalling_constraints.append(rule.copy())

    for x_a in range(2):
        for a in range(3):
            rule = [0]*(2*2*3*3 + 1)
            rule[18*x_a +     3*a +     1] = 1
            rule[18*x_a + 9 + 3*a +     1] = 1
            rule[18*x_a +     3*a + 1 + 1] = -1
            rule[18*x_a + 9 + 3*a + 1 + 1] = -1
            nosignalling_constraints.append(rule.copy())

            rule = [0]*(2*2*3*3 + 1)
            rule[18*x_a +     3*a + 1 + 1] = 1
            rule[18*x_a + 9 + 3*a + 1 + 1] = 1
            rule[18*x_a +     3*a + 2 + 1] = -1
            rule[18*x_a + 9 + 3*a + 2 + 1] = -1
            nosignalling_constraints.append(rule.copy())

    matrix.extend(nosignalling_constraints, linear = True)

    distribution_constraints = []
    for i in range(9):
        rule = [0] * (2*2*3*3 + 1)
        rule[0] = 1
        for j in range(4):
            rule[j*9 + i + 1] = -1
        distribution_constraints.append(rule.copy())

    matrix.extend(distribution_constraints, linear = True)

    matrix.rep_type = cdd.RepType.INEQUALITY
    matrix.canonicalize()
    poly = cdd.Polyhedron(matrix)

    with open('two_player_ab3_vertices.txt', 'w') as f:
        f.write(str(poly.get_generators()))

def two_players_xa3():
    """
    This function finds the vertices of the extreme points of the no-signalling polytope for three players each
    with binary input but |A| = 3. It writes the results to a file. It works very similar to three_players(). ordering
    of the variables becomes a bit more of a hassle.
    """

    # each variable q(x_a, x_b | a, b) is at place 18x_a + 6x_b + 2a + b in the list... so there are 9*4
    # variables in the list and one more value for b of [b  -A].
    positivity = []
    for i in range(3*3*3*2):
        rule = [0] * (3*3*3*2 + 1)
        rule[i+1] = 1
        positivity.append(rule.copy())

    matrix = cdd.Matrix(positivity)

    nosignalling_constraints = []
    for x_b in range(3):
        for b in range(2):
            rule = [0]*(3*3*3*2 + 1)
            rule[       6*x_b +     b + 1] = 1
            rule[18   + 6*x_b +     b + 1] = 1
            rule[18*2 + 6*x_b +     b + 1] = 1
            rule[     + 6*x_b + 2 + b + 1] = -1
            rule[18   + 6*x_b + 2 + b + 1] = -1
            rule[18*2 + 6*x_b + 2 + b + 1] = -1
            nosignalling_constraints.append(rule.copy())

            rule = [0]*(3*3*3*2 + 1)
            rule[       6*x_b + 2   + b + 1] = 1
            rule[18   + 6*x_b + 2   + b + 1] = 1
            rule[18*2 + 6*x_b + 2   + b + 1] = 1
            rule[     + 6*x_b + 2*2 + b + 1] = -1
            rule[18   + 6*x_b + 2*2 + b + 1] = -1
            rule[18*2 + 6*x_b + 2*2 + b + 1] = -1
            nosignalling_constraints.append(rule.copy())

    for x_a in range(3):
        for a in range(3):
            rule = [0]*(3*3*3*2 + 1)
            rule[18*x_a +       2*a +     1] = 1
            rule[18*x_a + 6   + 2*a +     1] = 1
            rule[18*x_a + 6*2 + 2*a +     1] = 1
            rule[18*x_a +       2*a + 1 + 1] = -1
            rule[18*x_a + 6   + 2*a + 1 + 1] = -1
            rule[18*x_a + 6*2 + 2*a + 1 + 1] = -1
            nosignalling_constraints.append(rule.copy())

    matrix.extend(nosignalling_constraints, linear = True)

    distribution_constraints = []
    for i in range(6):
        rule = [0] * (3*3*3*2 + 1)
        rule[0] = 1
        for j in range(9):
            rule[j*6 + i + 1] = -1
        distribution_constraints.append(rule.copy())

    matrix.extend(distribution_constraints, linear = True)

    matrix.rep_type = cdd.RepType.INEQUALITY
    matrix.canonicalize()
    poly = cdd.Polyhedron(matrix)

    with open('two_player_xa3_vertices.txt', 'w') as f:
        f.write(str(poly.get_generators()))

# This function probably takes way to long
def two_players_x4():
    """
    This function finds the vertices of the extreme points of the no-signalling polytope for three players each
    with binary input but |X| = 4. It writes the results to a file. It works very similar to three_players(). ordering
    of the variables becomes a bit more of a hassle.
    """

    # each variable q(x_a, x_b | a, b) is at place (4x_a + x_b) * 4 + (2a + b) + 1 in the list... so there are 9*4
    # variables in the list and one more value for b of [b  -A].
    positivity = []
    for i in range(16*4):
        rule = [0] * (16*4 + 1)
        rule[i+1] = 1
        positivity.append(rule.copy())

    matrix = cdd.Matrix(positivity)

    nosignalling_constraints = []
    for x_b in range(4):
        for b in range(2):
            rule = [0]*(16*4 + 1)
            rule[x_b       * 4 + b       + 1] = 1
            rule[(4 + x_b) * 4 + b       + 1] = 1
            rule[(8 + x_b) * 4 + b       + 1] = 1
            rule[(12 + x_b) * 4 + b       + 1] = 1
            rule[x_b       * 4 + (2 + b) + 1] = -1
            rule[(4 + x_b) * 4 + (2 + b) + 1] = -1
            rule[(8 + x_b) * 4 + (2 + b) + 1] = -1
            rule[(12 + x_b) * 4 + (2 + b) + 1] = -1
            nosignalling_constraints.append(rule.copy())

    for x_a in range(4):
        for a in range(2):
            rule = [0]*(16*4 + 1)
            rule[(4 * x_a)     * 4 + (2*a)     + 1] = 1
            rule[(4 * x_a + 1) * 4 + (2*a)     + 1] = 1
            rule[(4 * x_a + 2) * 4 + (2*a)     + 1] = 1
            rule[(4 * x_a + 3) * 4 + (2*a)     + 1] = 1
            rule[(4 * x_a)     * 4 + (2*a + 1) + 1] = -1
            rule[(4 * x_a + 1) * 4 + (2*a + 1) + 1] = -1
            rule[(4 * x_a + 2) * 4 + (2*a + 1) + 1] = -1
            rule[(4 * x_a + 3) * 4 + (2*a + 1) + 1] = -1
            nosignalling_constraints.append(rule.copy())

    matrix.extend(nosignalling_constraints, linear = True)

    distribution_constraints = []
    for i in range(4):
        rule = [0] * (16*4 + 1)
        rule[0] = 1
        for j in range(16):
            rule[j*4 + i + 1] = -1
        distribution_constraints.append(rule.copy())

    matrix.extend(distribution_constraints, linear = True)

    matrix.rep_type = cdd.RepType.INEQUALITY
    matrix.canonicalize()
    poly = cdd.Polyhedron(matrix)

    with open('two_player_x4_vertices.txt', 'w') as f:
        f.write(str(poly.get_generators()))



if __name__ == "__main__":
    #two_players()
    #three_players()
    #two_players_x3()
    #two_players_x4()
    #two_players_a3()
    #two_players_ab3()
    two_players_xa3()