from tests.__init__ import *

trefoil = Diagram([
    (2, 5, 3, 6),
    (4, 1, 5, 2),
    (6, 3, 1, 4),
])

figure8 = Diagram([
    (1, 6, 2, 7),
    (3, 1, 4, 8),
    (5, 2, 6, 3),
    (7, 5, 8, 4),
])

def test_trefoil_edge_1():
    assert twist(trefoil, 1) == Diagram(
        [(2, 2, 3, 1), (4, 7, 5, 8), (6, 3, 7, 4), (8, 5, 1, 6)]
    )

def test_trefoil_edge_2():
    assert twist(trefoil, 2) == Diagram(
        [(3, 3, 4, 2), (4, 7, 5, 8), (6, 1, 7, 2), (8, 5, 1, 6)]
    )

def test_trefoil_edge_3():
    assert twist(trefoil, 3) == Diagram(
        [(2, 7, 3, 8), (4, 4, 5, 3), (6, 1, 7, 2), (8, 5, 1, 6)]
    )

def test_trefoil_edge_4():
    assert twist(trefoil, 4) == Diagram(
        [(2, 7, 3, 8), (5, 5, 6, 4), (6, 1, 7, 2), (8, 3, 1, 4)]
    )

def test_trefoil_edge_5():
    assert twist(trefoil, 5) == Diagram(
        [(2, 7, 3, 8), (4, 1, 5, 2), (6, 6, 7, 5), (8, 3, 1, 4)]
    )

def test_trefoil_edge_6():
    assert twist(trefoil, 6) == Diagram(
        [(2, 5, 3, 6), (4, 1, 5, 2), (7, 7, 8, 6), (8, 3, 1, 4)]
    )

def test_figure8_edge_1():
    assert twist(figure8, 1) == Diagram(
        [(2, 2, 3, 1), (3, 8, 4, 9), (5, 1, 6, 10), (7, 4, 8, 5), (9, 7, 10, 6)]
    )
