from test.__init__ import *

trefoil = Diagram([
    (2, 5, 3, 6),
    (4, 1, 5, 2),
    (6, 3, 1, 4),
])

class TestPoke(unittest.TestCase):
    def test_trefoil_to_star_1_4(self):
        self.assertEqual(trefoil.poke(1, 4), Diagram([
            (2, 7, 3, 8), (3, 9, 4, 8), (4, 9, 5, 10), (6, 1, 7, 2), (10, 5, 1, 6)
        ]))

    def test_trefoil_to_star_4_1(self):
        self.assertEqual(trefoil.poke(4, 1), Diagram([
            (2, 7, 3, 8), (3, 9, 4, 8), (4, 9, 5, 10), (6, 1, 7, 2), (10, 5, 1, 6)
        ]))

    def test_trefoil_to_star_2_5(self):
        self.assertEqual(trefoil.poke(2, 5), Diagram([
            (2, 7, 3, 8), (3, 9, 4, 8), (4, 9, 5, 10), (6, 1, 7, 2), (10, 5, 1, 6)
        ]))

    def test_trefoil_to_star_5_2(self):
        self.assertEqual(trefoil.poke(5, 2), Diagram([
            (2, 7, 3, 8), (3, 9, 4, 8), (4, 9, 5, 10), (6, 1, 7, 2), (10, 5, 1, 6)
        ]))

    def test_trefoil_to_star_3_6(self):
        self.assertEqual(trefoil.poke(3, 6), Diagram([
            (2, 7, 3, 8), (3, 9, 4, 8), (4, 9, 5, 10), (6, 1, 7, 2), (10, 5, 1, 6)
        ]))

    def test_trefoil_to_star_6_3(self):
        self.assertEqual(trefoil.poke(6, 3), Diagram([
            (2, 7, 3, 8), (3, 9, 4, 8), (4, 9, 5, 10), (6, 1, 7, 2), (10, 5, 1, 6)
        ]))
