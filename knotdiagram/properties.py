from itertools import product
from knotdiagram.diagram import *

# Return the Gauss code of a diagram.
def get_gauss_code(self: Diagram) -> list[int]:
    raise NotImplementedError

# Return the Dowker-Thistlethwait notation of a diagram.
def get_dt_notation(self: Diagram) -> list[int]:
    raise NotImplementedError

# Return the Kauffman bracket of a diagram.
def get_kauffman_bracket(self: Diagram) -> KnotPoly:
    if self == Diagram([]): return KnotPoly({0: 1})

    factored_poly = [(((a, d), (b, c)), ((a, b), (c, d))) for a, b, c, d in self.pd_code]

    distributed_poly = [(sum(1-2*i for i in ii), [factor for term in terms for factor in term]) for ii, terms in zip(product(*(range(2) for _ in factored_poly)), product(*factored_poly))]

    for power, term in distributed_poly:
        matched_at_all = True
        while matched_at_all:
            matched_at_all = False
            i = 0
            if len(term) == 1: break
            while i < len(term):
                j = i + 1
                while j < len(term):
                    x1, x2 = term[i], term[j]
                    a1, b1 = x1
                    a2, b2 = x2

                    matched = True

                    if a1 == b2 and a2 == b1 or a1 == a2 and b1 == b2:
                        term.append((a1, a1))
                    elif a1 == a2:
                        term.append((b1, b2))
                    elif a1 == b2:
                        term.append((b1, a2))
                    elif b1 == a2:
                        term.append((a1, b2))
                    elif b1 == b2:
                        term.append((a1, a2))
                    else:
                        matched = False

                    if matched: del term[j], term[i]
                    if matched: matched_at_all = True
                    j += 1
                i += 1

    newlist = [(power, len(term)-1) for power, term in distributed_poly]

    disjoint_unknot_poly = KnotPoly({2: -1, -2: -1})

    return sum((KnotPoly({power1: 1}) * disjoint_unknot_poly**power2 for power1, power2 in newlist), KnotPoly.zero())

def get_writhe(self: Diagram) -> int:
    writhe = 0
    for _, b, _, d in self.pd_code:
        if self._next(b) == d:
            writhe -= 1
        else:
            writhe += 1
    return writhe

# Return the Jones polynomial of a diagram.
def get_jones_polynomial(self: Diagram) -> KnotPoly:
    writhe = get_writhe(self)
    kauffman_bracket = get_kauffman_bracket(self)
    raw_jones_polynomial = kauffman_bracket * KnotPoly({3*writhe: 1 if writhe % 2 == 0 else -1})
    coefficients = {powers[0]/4: coefficients for powers, coefficients in raw_jones_polynomial.coefficients.items()}
    return KnotPoly(coefficients)

# Return the list of edges.
def get_edges(self: Diagram) -> list[Edge]:
    return [i + 1 for i in range(2 * len(self.pd_code))]