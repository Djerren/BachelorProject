import cdd

def three_players():
    positivity = []
    for i in range(2**6):
        rule = [0] * (2**6 + 1)
        rule[i+1] = 1
        positivity.append(rule.copy())

    matrix = cdd.Matrix(positivity)

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

    matrix.extend(nosignalling_constraints, linear = True)

    distribution_constraints = []
    for i in range(2**3):
        condition = '{0:03b}'.format(i)
        rule = [0] * (2**6 + 1)
        rule[0] = 1
        for j in range(2**3):
            outcome = '{0:03b}'.format(j)
            rule[int(outcome + condition, 2) + 1] = -1
        distribution_constraints.append(rule.copy())

    matrix.extend(distribution_constraints, linear = True)
    matrix.rep_type = cdd.RepType.INEQUALITY
    matrix.canonicalize()
    poly = cdd.Polyhedron(matrix)
    with open('three_player_vertices.txt', 'w') as f:
        f.write(str(poly.get_generators()))

def two_players():
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