import unknotter as ut

# UNKNOT SOLVER

thwt = ut.THISTLETHWAITE_UNKNOT
ut.unknot_solver(thwt, 2)

trefoil = ut.knot(3, 1)
ut.unknot_solver(trefoil, 2)

figure8 = ut.knot(4, 1)
ut.unknot_solver(figure8, 2)

bigknot = ut.knot(9, 15)
ut.unknot_solver(bigknot, 2)

myknot = ut.knot(0, 1)
target_jones = ut.kauffman_bracket(myknot)
print('Target Jones:', target_jones)
for _ in range(1000):
    myknot = ut.apply_random_move(myknot, 1)
    jones = ut.kauffman_bracket(myknot)
    # if jones != target_jones:
    print('Writhe:', ut.get_writhe(myknot))
    print('Jones:', jones.var('A'))
    print('Knot:', myknot)
