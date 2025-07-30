import unknotter as ut
import sys

if len(sys.argv) != 4:
    print("Expected `python3 genknot.py <knot 0-4> <# crossings> <data size>`.")
    sys.exit(1)

knotid = int(sys.argv[1])
crossing_count = int(sys.argv[2])
data_size = int(sys.argv[3])

knot_choices = list(ut.first_n_knots(knotid+1))

knots: list[ut.Diagram] = []
for i in range(data_size):
    knot = knot_choices[-1][1]
    while len(knot.pd_code) < crossing_count:
        knot = ut.apply_random_move(knot, 0)
    knots.append(knot)

data = [[knot_choices[-1][0], ut.get_plaintext_code(knot)] for i, knot in enumerate(knots)]

print('\n'.join(','.join(line) for line in data))
