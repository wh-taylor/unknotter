from knotdiagram.diagram import *

# Get a list of all crossings that are adjacent to a given edge.
def _get_crossings_with_edge(self: Diagram, edge: Edge) -> list[Crossing]:
    return [crossing for crossing in self.pd_code if edge in crossing]

# Shift an edge by a given amount, wrapping around the number of edges.
def _shiftmod(self: Diagram, edge: Edge, n: int) -> Edge:
    return (edge + n - 1) % (2*len(self.pd_code)) + 1

# Get the edge after a given edge (+1 with wraparound).
def _next(self: Diagram, edge: Edge) -> Edge:
    return _shiftmod(self, edge, 1)

# Get the edge before a given edge (-1 with wraparound).
def _prev(self: Diagram, edge: Edge) -> Edge:
    return _shiftmod(self, edge, -1)

# Given the index of an edge, get the index of its friend.
# Say we have two crossings: (_, _, _, 2), (_, _, 2, _).
# The first 2 is in the first crossing in the fourth position, so it has the index (1, 4).
# The second 2 is in the second crossing in the third position, so it has the index (2, 3).
# Thus, diagram._get_friend_index(1, 4) = (2, 3) and diagram._get_friend_index(2, 3) = (1, 4).
def _get_friend_index(self: Diagram, crossing_index: int, edge_index: int) -> tuple[int, int]:
    edge = self.pd_code[crossing_index][edge_index]
    crossings_with_edge = _get_crossings_with_edge(self, edge)
    
    if len(crossings_with_edge) == 1:
        pos = [i for i, row in enumerate(self.pd_code[crossing_index]) if row == edge]
        return (crossing_index, pos[1] if pos[0] == edge_index else pos[0])
    
    if crossings_with_edge[0] == self.pd_code[crossing_index]:
        return (next(i for i, row in enumerate(self.pd_code) if row == crossings_with_edge[1]), next(i for i, x in enumerate(crossings_with_edge[1]) if x == edge))

    return (next(i for i, row in enumerate(self.pd_code) if row == crossings_with_edge[0]), next(i for i, x in enumerate(crossings_with_edge[0]) if x == edge))

# Return a diagram with all of its edge values shifted up by `n` without wrapping around.
# This method is meant for adjusting a diagram to be combined with another.
def _shift_unbounded(self: Diagram, n: int) -> Diagram:
    return Diagram([tuple(edge + n for edge in crossing) for crossing in self.pd_code])


# Returns whether or not the given index represents an edge that is facing its crossing.
def _index_is_facing(self: Diagram, crossing_index: int, edge_index: int) -> bool:
    if edge_index == 0: return True
    if edge_index == 1:
        return self.pd_code[crossing_index][3] == _next(self, self.pd_code[crossing_index][1])
    if edge_index == 3:
        return self.pd_code[crossing_index][1] == _next(self, self.pd_code[crossing_index][3])

# Get the index of the given edge in the crossing it faces toward.
# Note: the edge index is never 2, since the edge would then be
# facing away from the crossing.
def _get_forth_index(self: Diagram, edge: Edge) -> tuple[int, int]:
    for crossing_index, crossing in enumerate(self.pd_code):
        if crossing[0] == edge:
            return crossing_index, 0
        if crossing[1] == edge and crossing[3] == _next(self, edge):
            return crossing_index, 1
        if crossing[3] == edge and crossing[1] == _next(self, edge):
            return crossing_index, 3
    raise NotImplementedError

# Get the two faces adjacent to the given edge.
# Following the direction the given edge is pointing, two faces can be extracted.
# One by only going counterclockwise and one by only going clockwise.
# Each face is given as a list of edges that are signed. Since we generate faces
# based on a specific direction, the edge is negative if it goes against the direction
# of the path we follow in generating the face.
def _get_adjacent_faces(self: Diagram, edge: Edge) -> tuple[list[SignedEdge], list[SignedEdge]]:
    face_ccw: list[SignedEdge] = [edge]
    face_cw: list[SignedEdge] = [edge]

    # Generate the counterclockwise face.
    crossing_index, edge_index = _get_forth_index(self, edge)
    edge_index = (edge_index - 1) % 4
    while self.pd_code[crossing_index][edge_index] != edge:
        sign = -1 if _index_is_facing(self, crossing_index, edge_index) else 1
        face_ccw.append(sign * self.pd_code[crossing_index][edge_index])
        crossing_index, edge_index = _get_friend_index(self, crossing_index, edge_index)
        edge_index = (edge_index - 1) % 4
    
    # Generate the clockwise face.
    crossing_index, edge_index = _get_forth_index(self, edge)
    edge_index = (edge_index + 1) % 4
    while self.pd_code[crossing_index][edge_index] != edge:
        sign = -1 if _index_is_facing(self, crossing_index, edge_index) else 1
        face_cw.append(sign * self.pd_code[crossing_index][edge_index])
        crossing_index, edge_index = _get_friend_index(self, crossing_index, edge_index)
        edge_index = (edge_index + 1) % 4

    return (face_ccw, face_cw)

# An edge is closed if, on both of the crossings it connects to, it crosses underneath.
def _is_closed(self: Diagram, edge: Edge) -> bool:
    adj_crossings = [crossing for crossing in self.pd_code if edge in crossing]
    return edge in [adj_crossings[0][0], adj_crossings[0][2]] and edge in [adj_crossings[1][0], adj_crossings[1][2]]

# An edge is open if, on both of the crossings it connects to, it crosses over.
def _is_open(self: Diagram, edge: Edge) -> bool:
    adj_crossings = [crossing for crossing in self.pd_code if edge in crossing]
    return (edge in [adj_crossings[0][1], adj_crossings[0][3]]) and (edge in [adj_crossings[1][1], adj_crossings[1][3]])

# An edge is half-open if it crosses over one of its crossings and under the other.
def _is_half_open(self: Diagram, edge: Edge) -> bool:
    return not _is_open(self, edge) and not _is_closed(self, edge)
