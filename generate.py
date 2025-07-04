import unknotter as ut

import csv

n = 2
crossings = 10
logAll = False
log1000 = True

knot_choices = list(ut.first_n_knots(n))

knots: list[ut.Diagram] = []
for i in range(50000):
    knot = knot_choices[i % n][1]
    while len(knot.pd_code) < 10:
        knot = ut.apply_random_move(knot, 0)
    knots.append(knot)
    if logAll:
        print(knot_choices[i % n][0], '| Length:', len(knot.pd_code), 'Index:', i+1)
    if log1000 and i % 1000 == 0:
        print(knot_choices[i % n][0], '| Length:', len(knot.pd_code), 'Index:', i+1)

data = [
    ['Knot', 'Code'],
] + [[knot_choices[i % n][0], ut.get_plaintext_code(knot)] for i, knot in enumerate(knots)]

with open('training2_10x.csv', 'w', newline='') as file:
    csv.writer(file).writerows(data)