from __future__ import annotations
from knotdiagram.polynomial import *

Edge = int
SignedEdge = int
Crossing = tuple[Edge, Edge, Edge, Edge]
PDNotation = list[Crossing]

class ReidemeisterError(Exception):
    pass

class Diagram:
    def __init__(self, pd_code):
        self.pd_code: PDNotation = pd_code
    
    def __repr__(self) -> str:
        return f'Diagram({repr(self.pd_code)})'
    
    # Check if a diagram is equivalent to another considering orientation.
    def __eq__(self, other: Diagram) -> Diagram:
        if self.pd_code == other.pd_code: return True
        for n in range(2*len(self.pd_code)):
            if self.shift(n).identical(other):
                return True
        return False
    
    # Shift an edge by a given amount, wrapping around the number of edges.
    def _shiftmod(self, edge: Edge, n: int) -> Edge:
        return (edge + n - 1) % (2*len(self.pd_code)) + 1

    # Return a diagram with all of its edge values shifted up by `n`.
    def shift(self: Diagram, n: int) -> Diagram:
        return Diagram([tuple(self._shiftmod(edge, n) for edge in crossing) for crossing in self.pd_code])

    # Return true if and only if all edge values of both diagrams are completely identical.
    def identical(self: Diagram, other: Diagram) -> bool:
        if len(self.pd_code) != len(other.pd_code): return False
        return set(self.pd_code) == set(other.pd_code)
