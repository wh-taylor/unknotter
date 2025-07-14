import unknotter as ut
import sys

if len(sys.argv) != 4:
    print("Expected `python3 generate.py <# knots> <# crossings> <data size>`.")
    sys.exit(1)

knot_count = int(sys.argv[1])
crossing_count = int(sys.argv[2])
data_size = int(sys.argv[3])

knot_choices = list(ut.first_n_knots(knot_count))

knot_count: list[ut.Diagram] = []
for i in range(data_size):
    knot = knot_choices[i % knot_count][1]
    while len(knot.pd_code) < crossing_count:
        knot = ut.apply_random_move(knot, 0)
    knot_count.append(knot)

data = [[knot_choices[i % knot_count][0], ut.get_plaintext_code(knot)] for i, knot in enumerate(knot_count)]

print('\n'.join(','.join(line) for line in data))
