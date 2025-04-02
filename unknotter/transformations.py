from unknotter.diagram import *

def reverse(self: Diagram) -> Diagram:
    """Return a diagram with opposite orientation of `diagram`."""
    return Diagram([(d, c, b, a) for (a, b, c, d) in self.pd_code])

def reflect(self: Diagram) -> Diagram:
    """Return a diagram of the reflection of the link of `diagram`."""
    return Diagram([(a, d, c, b) for (a, b, c, d) in self.pd_code])

def disjoint_union(self: Diagram) -> Diagram:
    """Return the disjoint union of two diagrams."""
    raise NotImplementedError

def join(self: Diagram, other: Diagram, self_edge: Edge, other_edge: Edge) -> Diagram:
    """Return the joining of two diagrams by given edges (generalizes connected sum)."""
    raise NotImplementedError
