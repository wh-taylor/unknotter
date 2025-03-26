from knotdiagram.diagram import *
from knotdiagram.utils import _shiftmod

# Return the Gauss code of a diagram.
def get_gauss_code(self: Diagram) -> list[int]:
    raise NotImplementedError

# Return the Dowker-Thistlethwait notation of a diagram.
def get_dt_notation(self: Diagram) -> list[int]:
    raise NotImplementedError

# Return a diagram with all of its edge values shifted up by `n`.
def shift(self: Diagram, n: int) -> Diagram:
    return Diagram([tuple(_shiftmod(self, edge, n) for edge in crossing) for crossing in self.pd_code])

# Return a diagram with opposite orientation of `diagram`.
def reverse(self: Diagram) -> Diagram:
    return Diagram([(d, c, b, a) for (a, b, c, d) in self.pd_code])

# Return a diagram of the reflection of the link of `diagram`.
def reflect(self: Diagram) -> Diagram:
    return Diagram([(a, d, c, b) for (a, b, c, d) in self.pd_code])

# Return true if and only if all edge values of both diagrams are completely identical.
def identical(self: Diagram, other: Diagram) -> bool:
    if len(self.pd_code) != len(other.pd_code): return False
    return set(self.pd_code) == set(other.pd_code)

# Check if a diagram is equivalent to another considering orientation.
def equals(self: Diagram, diagram2: Diagram):
    if self.pd_code == diagram2.pd_code: return True
    for n in range(2*len(self.pd_code)):
        if identical(shift(self, n), diagram2):
            return True
    return False

# Check if a diagram is equivalent to another up to orientation.
# Two knows with reverse orientations are "congruent".
def is_congruent(self: Diagram, diagram2: Diagram):
    for n in range(2*len(self.pd_code)):
        if identical(shift(self, n), diagram2) or identical(shift(reverse(self), n), diagram2):
            return True
    return False

# Return the disjoint union of two diagrams.
def disjoint_union(self: Diagram) -> Diagram:
    raise NotImplementedError

# Return the joining of two diagrams by given edges (generalizes connected sum).
def join(self: Diagram, other: Diagram, self_edge: Edge, other_edge: Edge) -> Diagram:
    raise NotImplementedError
