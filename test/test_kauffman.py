from test.__init__ import *

class TestPositiveTwist(unittest.TestCase):
    def test_trefoil_bracket(self):
        self.assertEqual(
            knot(3, 1).get_kauffman_bracket(),
            KnotPoly({-5: -1, 3: -1, 7: 1})
        )

    def test_figure8_bracket(self):
        self.assertEqual(
            knot(4, 1).get_kauffman_bracket(),
            KnotPoly({-8: 1, -4: -1, 0: 1, 4: -1, 8: 1})
        )

    def test_trefoil_preserve_poke(self):
        self.assertEqual(
            knot(3, 1).get_kauffman_bracket(),
            knot(3, 1).poke(1, 4).get_kauffman_bracket()
        )
        self.assertEqual(
            knot(3, 1).get_kauffman_bracket(),
            knot(3, 1).poke(2, 5).get_kauffman_bracket()
        )
        self.assertEqual(
            knot(3, 1).get_kauffman_bracket(),
            knot(3, 1).poke(3, 6).get_kauffman_bracket()
        )
    
    def test_figure8_preserve_poke(self):
        self.assertEqual(
            knot(4, 1).get_kauffman_bracket(),
            knot(4, 1).poke(1, 4).get_kauffman_bracket()
        )
        self.assertEqual(
            knot(4, 1).get_kauffman_bracket(),
            knot(4, 1).poke(3, 8).get_kauffman_bracket()
        )
        self.assertEqual(
            knot(4, 1).get_kauffman_bracket(),
            knot(4, 1).poke(2, 5).get_kauffman_bracket()
        )
