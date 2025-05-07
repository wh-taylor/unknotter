from itertools import product
from unknotter.diagram import *

def gauss_code(self: Diagram) -> list[int]:
    """Return the Gauss code of a diagram."""
    raise NotImplementedError

def dt_notation(self: Diagram) -> list[int]:
    """Return the Dowker-Thistlethwait notation of a diagram."""
    raise NotImplementedError

def kauffman_bracket(self: Diagram) -> Polynomial:
    """Return the Kauffman bracket polynomial of a diagram."""
    if self == Diagram([(1, 1, 2, 2)]): return Polynomial({3: -1})

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

    disjoint_unknot_poly = Polynomial({2: -1, -2: -1})

    return sum((Polynomial({power1: 1}) * disjoint_unknot_poly**power2 for power1, power2 in newlist), Polynomial.zero())

def get_writhe(self: Diagram) -> int:
    """Return the writhe of a diagram."""
    writhe = 0
    for _, b, _, d in self.pd_code:
        if self._next(b) == d:
            writhe -= 1
        else:
            writhe += 1
    return writhe

def jones(self: Diagram) -> Polynomial:
    """Return the Jones polynomial of a diagram."""
    writhe = get_writhe(self)
    bracket = kauffman_bracket(self)
    raw_jones_polynomial = bracket * Polynomial({3*writhe: 1 if writhe % 2 == 0 else -1})
    coefficients = {powers[0]/4: coefficients for powers, coefficients in raw_jones_polynomial.coefficients.items()}
    return Polynomial(coefficients)

def get_edges(self: Diagram) -> list[Edge]:
    """Return a list of all edges in a diagram with their integer values."""
    return [i + 1 for i in range(2 * len(self.pd_code))]

def is_infinity_unknot(self: Diagram) -> bool:
    return self == Diagram([(1, 2, 2, 1)]) or self == Diagram([(2, 2, 1, 1)])

def _is_valid(self: Diagram) -> bool:
    edges = get_edges(self)
    for crossing in self.pd_code:
        for edge in crossing:
            if edge not in edges:
                return False
    for edge in edges:
        edge_count = 0
        for crossing in self.pd_code:
            edge_count += crossing.count(edge)
        if edge_count != 2:
            return False
    return True
