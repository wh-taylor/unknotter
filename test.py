import unittest
from catalog import *
from diagram import Diagram
from polynomial import KnotPoly

class TestKauffmanBracket(unittest.TestCase):
    def test_unknot_bracket(self):
        unknot = knot(0, 1)
        expected_polynomial = KnotPoly({0: 1})
        self.assertEqual(unknot.get_kauffman_bracket(), expected_polynomial)

if __name__ == '__main__':
    unittest.main()
