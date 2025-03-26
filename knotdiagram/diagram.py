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

        from knotdiagram.operators import equals
        self._equals = equals
    
    def __repr__(self) -> Diagram:
        return 'PD [ ' + ',\n     '.join('(' + ', '.join(str(e) for e in crossing) + ')' for crossing in self.pd_code) + ' ]'
    
    def __eq__(self, other: Diagram) -> Diagram:
        return self._equals(self, other)

