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
    
    def __eq__(self, other: Diagram) -> Diagram:
        """Check if a diagram is equivalent to another considering orientation."""
        if self.pd_code == other.pd_code: return True
        for n in range(2*len(self.pd_code)):
            if self.shift(n).identical(other):
                return True
        return False
    
    def _shiftmod(self, edge: Edge, n: int) -> Edge:
        """Shift an edge by a given amount, wrapping around the number of edges."""
        return (edge + n - 1) % (2*len(self.pd_code)) + 1

    def shift(self, n: int) -> Diagram:
        """Return a diagram with all of its edge values shifted up by `n`."""
        return Diagram([tuple(self._shiftmod(edge, n) for edge in crossing) for crossing in self.pd_code])

    def identical(self, other: Diagram) -> bool:
        """Return true if and only if all edge values of both diagrams are completely identical."""
        if len(self.pd_code) != len(other.pd_code): return False
        return set(self.pd_code) == set(other.pd_code)

    def _get_crossings_with_edge(self, edge: Edge) -> list[Crossing]:
        """Get a list of all crossings that are adjacent to a given edge."""
        return [crossing for crossing in self.pd_code if edge in crossing]

    def _next(self, edge: Edge) -> Edge:
        """Get the edge after a given edge (+1 with wraparound)."""
        return self._shiftmod(edge, 1)

    def _prev(self, edge: Edge) -> Edge:
        """Get the edge before a given edge (-1 with wraparound)."""
        return self._shiftmod(edge, -1)

    def _get_friend_index(self, crossing_index: int, edge_index: int) -> tuple[int, int]:
        """Given the index of an edge, get the index of its friend.

        Say we have two crossings: (_, _, _, 2), (_, _, 2, _).
        The first 2 is in the first crossing in the fourth position, so it has the index (1, 4).
        The second 2 is in the second crossing in the third position, so it has the index (2, 3).
        Thus, diagram._get_friend_index(1, 4) = (2, 3) and diagram._get_friend_index(2, 3) = (1, 4).
        """
        edge = self.pd_code[crossing_index][edge_index]
        crossings_with_edge = self._get_crossings_with_edge(edge)
        
        if len(crossings_with_edge) == 1:
            pos = [i for i, row in enumerate(self.pd_code[crossing_index]) if row == edge]
            return (crossing_index, pos[1] if pos[0] == edge_index else pos[0])
        
        if crossings_with_edge[0] == self.pd_code[crossing_index]:
            return (next(i for i, row in enumerate(self.pd_code) if row == crossings_with_edge[1]), next(i for i, x in enumerate(crossings_with_edge[1]) if x == edge))

        return (next(i for i, row in enumerate(self.pd_code) if row == crossings_with_edge[0]), next(i for i, x in enumerate(crossings_with_edge[0]) if x == edge))

    def _shift_unbounded(self, n: int) -> Diagram:
        """Return a diagram with all of its edge values shifted up by `n` without wrapping around.

        This method is meant for adjusting a diagram to be combined with another.
        """
        return Diagram([tuple(edge + n for edge in crossing) for crossing in self.pd_code])

    def _index_is_facing(self, crossing_index: int, edge_index: int) -> bool:
        """Returns whether or not the given index represents an edge that is facing its crossing."""
        if edge_index == 0: return True
        if edge_index == 1:
            return self.pd_code[crossing_index][3] == self._next(self.pd_code[crossing_index][1])
        if edge_index == 3:
            return self.pd_code[crossing_index][1] == self._next(self.pd_code[crossing_index][3])

    def _get_forth_index(self, edge: Edge) -> tuple[int, int]:
        """Get the index of the given edge in the crossing it faces toward.

        Note: the edge index is never 2, since the edge would then be
        facing away from the crossing.
        """
        for crossing_index, crossing in enumerate(self.pd_code):
            if crossing[0] == edge:
                return crossing_index, 0
            if crossing[1] == edge and crossing[3] == self._next(edge):
                return crossing_index, 1
            if crossing[3] == edge and crossing[1] == self._next(edge):
                return crossing_index, 3
        raise NotImplementedError

    def _get_adjacent_faces(self, edge: Edge) -> tuple[list[SignedEdge], list[SignedEdge]]:
        """Get the two faces adjacent to the given edge.
        
        Following the direction the given edge is pointing, two faces can be extracted.
        One by only going counterclockwise and one by only going clockwise.
        Each face is given as a list of edges that are signed. Since we generate faces
        based on a specific direction, the edge is negative if it goes against the direction
        of the path we follow in generating the face.
        """
        face_ccw: list[SignedEdge] = [edge]
        face_cw: list[SignedEdge] = [edge]

        # Generate the counterclockwise face.
        crossing_index, edge_index = self._get_forth_index(edge)
        edge_index = (edge_index - 1) % 4
        while self.pd_code[crossing_index][edge_index] != edge:
            sign = -1 if self._index_is_facing(crossing_index, edge_index) else 1
            face_ccw.append(sign * self.pd_code[crossing_index][edge_index])
            crossing_index, edge_index = self._get_friend_index(crossing_index, edge_index)
            edge_index = (edge_index - 1) % 4
        
        # Generate the clockwise face.
        crossing_index, edge_index = self._get_forth_index(edge)
        edge_index = (edge_index + 1) % 4
        while self.pd_code[crossing_index][edge_index] != edge:
            sign = -1 if self._index_is_facing(crossing_index, edge_index) else 1
            face_cw.append(sign * self.pd_code[crossing_index][edge_index])
            crossing_index, edge_index = self._get_friend_index(crossing_index, edge_index)
            edge_index = (edge_index + 1) % 4

        return (face_ccw, face_cw)

    def _is_closed(self, edge: Edge) -> bool:
        """Check if an edge on a diagram is closed.
        
        An edge is closed if, on both of the crossings it connects to, it crosses underneath.
        """
        adj_crossings = [crossing for crossing in self.pd_code if edge in crossing]
        return edge in [adj_crossings[0][0], adj_crossings[0][2]] and edge in [adj_crossings[1][0], adj_crossings[1][2]]

    def _is_open(self, edge: Edge) -> bool:
        """Check if an edge on a diagram is open.
        
        An edge is open if, on both of the crossings it connects to, it crosses over.
        """
        adj_crossings = [crossing for crossing in self.pd_code if edge in crossing]
        return (edge in [adj_crossings[0][1], adj_crossings[0][3]]) and (edge in [adj_crossings[1][1], adj_crossings[1][3]])

    def _is_half_open(self, edge: Edge) -> bool:
        """Check if an edge on a diagram is half-open.
        
        An edge is half-open if it crosses over one of its crossings and under the other.
        """
        return not self._is_open(edge) and not self._is_closed(edge)
