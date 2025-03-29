from tests.__init__ import *

def test_trefoil_to_star_1_4():
    assert poke(knot(3, 1), 1, 4) == Diagram([
        (2, 7, 3, 8), (3, 9, 4, 8), (4, 9, 5, 10), (6, 1, 7, 2), (10, 5, 1, 6)
    ])

def test_trefoil_to_star_4_1():
    assert poke(knot(3, 1), 4, 1) == Diagram([
        (2, 7, 3, 8), (3, 9, 4, 8), (4, 9, 5, 10), (6, 1, 7, 2), (10, 5, 1, 6)
    ])

def test_trefoil_to_star_2_5():
    assert poke(knot(3, 1), 2, 5) == Diagram([
        (2, 7, 3, 8), (3, 9, 4, 8), (4, 9, 5, 10), (6, 1, 7, 2), (10, 5, 1, 6)
    ])

def test_trefoil_to_star_5_2():
    assert poke(knot(3, 1), 5, 2) == Diagram([
        (2, 7, 3, 8), (3, 9, 4, 8), (4, 9, 5, 10), (6, 1, 7, 2), (10, 5, 1, 6)
    ])

def test_trefoil_to_star_3_6():
    assert poke(knot(3, 1), 3, 6) == Diagram([
        (2, 7, 3, 8), (3, 9, 4, 8), (4, 9, 5, 10), (6, 1, 7, 2), (10, 5, 1, 6)
    ])

def test_trefoil_to_star_6_3():
    assert poke(knot(3, 1), 6, 3) == Diagram([
        (2, 7, 3, 8), (3, 9, 4, 8), (4, 9, 5, 10), (6, 1, 7, 2), (10, 5, 1, 6)
    ])

def test_infinity_unknot():
    assert poke(Diagram([(1, 2, 2, 1)]), 1, 2) == Diagram([(1, 4, 2, 5), (2, 6, 3, 5), (3, 6, 4, 1)])

def test_infinity_unknot_2():
    assert poke(Diagram([(1, 1, 2, 2)]), 2, 1) == Diagram([(4, 2, 5, 1), (5, 2, 6, 3), (6, 4, 1, 3)])
