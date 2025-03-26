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
    
    def __repr__(self) -> Diagram:
        return 'PD [ ' + ',\n     '.join('(' + ', '.join(str(e) for e in crossing) + ')' for crossing in self.pd_code) + ' ]'
    
    # from knotdiagram.reidemeister import (
    #     get_twistables,
    #     get_untwistables,
    #     get_pokables,
    #     get_unpokables,
    #     get_slidables,
    #     twist,
    #     untwist,
    #     poke,
    #     unpoke,
    #     slide,
    # )

    # from knotdiagram.properties import (
    #     get_kauffman_bracket,
    #     get_jones_polynomial,
    #     get_writhe,
    #     get_edges,
    # )

    # from knotdiagram.operators import (
    #     get_dt_notation,
    #     get_gauss_code,
    #     shift,
    #     reverse,
    #     reflect,
    #     identical,
    #     equals as __eq__,
    #     is_congruent,
    #     disjoint_union,
    #     join,
    # )
