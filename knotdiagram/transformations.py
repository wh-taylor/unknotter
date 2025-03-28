from knotdiagram.diagram import *

# Return a diagram with opposite orientation of `diagram`.
def reverse(self: Diagram) -> Diagram:
    return Diagram([(d, c, b, a) for (a, b, c, d) in self.pd_code])

# Return a diagram of the reflection of the link of `diagram`.
def reflect(self: Diagram) -> Diagram:
    return Diagram([(a, d, c, b) for (a, b, c, d) in self.pd_code])

# Return the disjoint union of two diagrams.
def disjoint_union(self: Diagram) -> Diagram:
    raise NotImplementedError

# Return the joining of two diagrams by given edges (generalizes connected sum).
def join(self: Diagram, other: Diagram, self_edge: Edge, other_edge: Edge) -> Diagram:
    raise NotImplementedError
