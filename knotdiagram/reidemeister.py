from knotdiagram.diagram import *
from knotdiagram.properties import get_edges
from knotdiagram.utils import (
    _get_adjacent_faces,
    _get_forth_index,
    _get_crossings_with_edge,
    _get_friend_index,
    _next,
    _prev,
    _is_closed,
    _is_open,
    _is_half_open
)

# Return the list of edges that can be twisted (which is all of them).
def get_twistables(self: Diagram) -> list[Edge]:
    return get_edges(self)

# Return the list of edges that can be untwisted.
def get_untwistables(self: Diagram) -> list[Edge]:
    untwistables = []
    for crossing in self.pd_code:
        if len(set(crossing)) == 3:
            untwistables.append(max(set(crossing), key=crossing.count))
    return untwistables

# Return the list of (ordered) pairs of edges that can be poked.
def get_pokables(self: Diagram) -> list[tuple[Edge, Edge]]:
    pokables = []
    for edge in get_edges(self):
        pokable_with = []
        face_ccw, face_cw = _get_adjacent_faces(self, edge)
        for signed_edge in face_ccw + face_cw:
            adj_edge = abs(signed_edge)
            if adj_edge != edge and adj_edge not in pokable_with:
                pokable_with.append(adj_edge)
        pokables += ((edge, e) for e in pokable_with)
    return pokables

# Return the list of (ordered) pairs of edges that can be unpoked.
def get_unpokables(self: Diagram) -> list[tuple[Edge, Edge]]:
    unpokables = []
    for edge in get_edges(self):
        if any(edge in pair for pair in unpokables):
            continue
        face_ccw, face_cw = _get_adjacent_faces(self, edge)
        if len(face_ccw) == 2 and is_unpokable(self, *[abs(n) for n in face_ccw]):
                unpokables.append(tuple(sorted(abs(n) for n in face_ccw)))
        if len(face_cw) == 2 and is_unpokable(self, *[abs(n) for n in face_cw]):
                unpokables.append(tuple(sorted(abs(n) for n in face_cw)))
    return unpokables

# Return the list of (ordered) triplets of edges that can be slid.
def get_slidables(self: Diagram) -> list[tuple[Edge, Edge, Edge]]:
    slidables = []
    for edge in get_edges(self):
        if any(edge in triplet for triplet in slidables):
            continue
        face_ccw, face_cw = _get_adjacent_faces(self, edge)
        if len(face_ccw) == 3 and is_slidable(self, *[abs(n) for n in face_ccw]):
                slidables.append(tuple(sorted(abs(n) for n in face_ccw)))
        if len(face_cw) == 3 and is_slidable(self, *[abs(n) for n in face_cw]):
                slidables.append(tuple(sorted(abs(n) for n in face_cw)))
    return slidables

# Readjust the edge values of `diagram` with the expectation of a twist at `target_edge`.
def _prepare_twist(self: Diagram, target_edge: Edge) -> PDNotation:
    pd_code: PDNotation = []

    # Map over each edge in each crossing of `diagram`.
    for crossing in self.pd_code:
        new_crossing_as_list: list[Edge] = []
        for edge in crossing:
            # If a given edge comes before the target edge, leave it alone.
            # If a given edge comes after the target edge, add two.
            # If it is the target edge, leave it alone if it connects with the
            #   previous edge or add two if it connects with the next edge.
            if edge < target_edge or edge == target_edge and _prev(self, edge) in crossing:
                new_crossing_as_list.append(edge)
            else:
                new_crossing_as_list.append(edge + 2)
        new_crossing: Crossing = tuple(new_crossing_as_list)
        pd_code.append(new_crossing)
    
    return pd_code

# Apply a positive twist on `target_edge`.
def _postwist(self: Diagram, target_edge: Edge) -> Diagram:
    pd_code = _prepare_twist(self, target_edge)
    pd_code.append((target_edge + 1, target_edge + 1, target_edge + 2, target_edge))
    return Diagram(pd_code)

# Apply a negative twist on `target_edge`.
def _negtwist(self: Diagram, target_edge: Edge) -> Diagram:
    pd_code = _prepare_twist(self, target_edge)
    pd_code.append((target_edge, target_edge + 1, target_edge + 1, target_edge + 2))
    return Diagram(pd_code)

# Twist `target_edge`.
def twist(self: Diagram, target_edge: Edge, is_positive: bool = True) -> Diagram:
    return _postwist(self, target_edge) if is_positive else _negtwist(self, target_edge)

# Remove the twist adjacent to the given edge.
def untwist(self: Diagram, edge: Edge) -> Diagram:
    pd_code: PDNotation = self.pd_code.copy()
    for i, crossing in enumerate(pd_code):
        if crossing.count(edge) == 2:
            del pd_code[i]
            break
    else:
        raise ReidemeisterError("given edge is not on a twist, so it cannot be untwisted.")
    pd_code = [tuple(e - 2 if e > edge else e for e in crossing) for crossing in pd_code]
    return Diagram(pd_code)

# Readjust the edge values of `diagram` with the expectation of a poke between the two edges.
def _prepare_poke(self: Diagram, lower_edge: Edge, higher_edge: Edge) -> PDNotation:
    pd_code: PDNotation = []

    # Map over each edge in each crossing of `diagram`.
    for crossing in self.pd_code:
        new_crossing_as_list: list[Edge] = []
        for edge in crossing:
            # If a given edge comes before the lower edge, leave it alone.
            # If a given edge is between the lower and higher edges, add two.
            # If a given edge comes after the higher edge, add four.
            # If it is the lower edge, leave it alone if it connects with the
            #   previous edge or add two if it connects with the next edge.
            # If it is the higher edge, add two if it connects with the previous
            #   edge or add four if it connects with the next edge.
            should_add_none = (
                edge < lower_edge or
                edge == lower_edge and _prev(self, edge) in crossing)
            should_add_two = (
                edge == lower_edge or
                lower_edge < edge < higher_edge or
                edge == higher_edge and _prev(self, edge) in crossing)

            if should_add_none:
                new_crossing_as_list.append(edge)
            elif should_add_two:
                new_crossing_as_list.append(edge + 2)
            else:
                new_crossing_as_list.append(edge + 4)
        new_crossing: Crossing = tuple(new_crossing_as_list)
        pd_code.append(new_crossing)

    return pd_code

# Poke `under_edge` underneath `over_edge`.
def poke(self: Diagram, under_edge: Edge, over_edge: Edge) -> Diagram:
    # Disallow poking an edge under itself.
    if under_edge == over_edge:
        raise ReidemeisterError("cannot poke an edge underneath iteself.")

    # Handle infinity unknots as special cases.
    if self == Diagram([(1, 2, 2, 1)]):
        if under_edge == 1 and over_edge == 2:
            return Diagram([(1, 4, 2, 5), (2, 6, 3, 5), (3, 6, 4, 1)])
        else:
            return Diagram([(4, 2, 5, 1), (5, 2, 6, 3), (3, 6, 4, 1)])
    elif self == Diagram([(2, 2, 1, 1)]):
        if under_edge == 1 and over_edge == 2:
            return Diagram([(1, 4, 2, 5), (2, 6, 3, 5), (6, 4, 1, 3)])
        else:
            return Diagram([(4, 2, 5, 1), (5, 2, 6, 3), (6, 4, 1, 3)])
    
    lower_edge = min(under_edge, over_edge)
    higher_edge = max(under_edge, over_edge)

    face_ccw, face_cw = _get_adjacent_faces(self, lower_edge)

    if not (higher_edge in face_cw or -higher_edge in face_cw or higher_edge in face_ccw or -higher_edge in face_ccw):
        raise ReidemeisterError("can only poke edges along the same face.")

    pd_code = _prepare_poke(self, lower_edge, higher_edge)
    
    # Add the two new crossings.
    if -higher_edge in face_cw:
        if under_edge == lower_edge:
            pd_code.append((lower_edge, higher_edge + 2, lower_edge + 1, higher_edge + 3))
            pd_code.append((lower_edge + 1, higher_edge + 4, lower_edge + 2, higher_edge + 3))
        else:
            pd_code.append((higher_edge + 2, lower_edge + 1, higher_edge + 3, lower_edge))
            pd_code.append((higher_edge + 3, lower_edge + 1, higher_edge + 4, lower_edge + 2))
    elif -higher_edge in face_ccw:
        if under_edge == lower_edge:
            pd_code.append((lower_edge, higher_edge + 3, lower_edge + 1, higher_edge + 2))
            pd_code.append((lower_edge + 1, higher_edge + 3, lower_edge + 2, higher_edge + 4))
        else:
            pd_code.append((higher_edge + 2, lower_edge, higher_edge + 3, lower_edge + 1))
            pd_code.append((higher_edge + 3, lower_edge + 2, higher_edge + 4, lower_edge + 1))
    elif higher_edge in face_cw:
        if under_edge == lower_edge:
            pd_code.append((lower_edge, higher_edge + 4, lower_edge + 1, higher_edge + 3))
            pd_code.append((lower_edge + 1, higher_edge + 2, lower_edge + 2, higher_edge + 3))
        else:
            pd_code.append((higher_edge + 2, lower_edge + 1, higher_edge + 3, lower_edge + 2))
            pd_code.append((higher_edge + 3, lower_edge + 1, higher_edge + 4, lower_edge))
    elif higher_edge in face_ccw:
        if under_edge == lower_edge:
            pd_code.append((lower_edge, higher_edge + 3, lower_edge + 1, higher_edge + 4))
            pd_code.append((lower_edge + 1, higher_edge + 3, lower_edge + 2, higher_edge + 2))
        else:
            pd_code.append((higher_edge + 2, lower_edge + 2, higher_edge + 3, lower_edge + 1))
            pd_code.append((higher_edge + 3, lower_edge, higher_edge + 4, lower_edge + 1))

    return Diagram(pd_code)

# Remove the poke between the two given edges.
def unpoke(self: Diagram, edge1: Edge, edge2: Edge) -> Diagram:
    pd_code: PDNotation = []
    deleted_crossings = 0
    for i, crossing in enumerate(self.pd_code):
        if edge1 in crossing and edge2 in crossing:
            deleted_crossings += 1
        else:
            pd_code.append(crossing)
    if deleted_crossings != 2:
        raise ReidemeisterError("given edge is not on a poke, so it cannot be unpoked.")
    lower_edge = min(edge1, edge2)
    higher_edge = max(edge1, edge2)
    pd_code = [tuple(e - 4 if e > higher_edge else e if e < lower_edge else e - 2 for e in crossing) for crossing in pd_code]
    return Diagram(pd_code)

def is_unpokable(self: Diagram, edge1: Edge, edge2: Edge) -> bool:
    return any((
        _is_open(self, edge1) and _is_closed(self, edge2),
        _is_open(self, edge2) and _is_closed(self, edge1),
    ))

def is_slidable(self: Diagram, edge1: Edge, edge2: Edge, edge3: Edge) -> bool:
    return any((
        _is_open(self, edge1) and _is_closed(self, edge2) and _is_half_open(self, edge3),
        _is_open(self, edge1) and _is_closed(self, edge3) and _is_half_open(self, edge2),
        _is_open(self, edge2) and _is_closed(self, edge1) and _is_half_open(self, edge3),
        _is_open(self, edge2) and _is_closed(self, edge3) and _is_half_open(self, edge1),
        _is_open(self, edge3) and _is_closed(self, edge1) and _is_half_open(self, edge2),
        _is_open(self, edge3) and _is_closed(self, edge2) and _is_half_open(self, edge1),
    ))

# Slide an edge over the face formed by the three given edges.
def slide(self: Diagram, edge1: Edge, edge2: Edge, edge3: Edge) -> Diagram:
    edges = [edge1, edge2, edge3]

    # Check if edges all lie on the same face
    face_ccw, face_cw = _get_adjacent_faces(self, edge1)
    if not (all(edge in face_ccw or -edge in face_ccw for edge in edges) and len(face_ccw) == 3 or all(edge in face_cw or -edge in face_cw for edge in edges) and len(face_cw) == 3):
        raise ReidemeisterError("can only slide three edges along the same face.")
    
    # Check if edges are layered properly
    if not is_slidable(self, edge1, edge2, edge3):
        raise ReidemeisterError("given edges do not follow the correct pattern for a slide.")

    # Initialize three crossings to be updated while iterating over the relevant crossings.
    pd_code = [[0, 0, 0, 0] for _ in range(len(self.pd_code))]

    # Map over each edge in each relevant crossing by index.
    # The crossing index is the index of a crossing in the PD notation as a list.
    for crossing_index in range(len(self.pd_code)):
        # The edge index is the index of an edge in a crossing.
        for edge_index in range(4):
            # Shift the relevant crossings down two. However, if the edge is one of the three edges forming the face of the slide, use the edge shifted down two from its friend instead.
            # See `_get_friend_index` for the definition of a friend.
            if any(edge in self.pd_code[crossing_index] for edge in edges) and self.pd_code[crossing_index][edge_index] in [edge1, edge2, edge3]:
                friend_crossing_index, friend_edge_index = _get_friend_index(self, crossing_index, edge_index)
                pd_code[crossing_index][edge_index] = (
                    self.pd_code[friend_crossing_index][(friend_edge_index + 2) % 4]
                )
            elif any(edge in self.pd_code[crossing_index] for edge in edges):
                pd_code[crossing_index][edge_index] = self.pd_code[crossing_index][(edge_index + 2) % 4]
            else:
                pd_code[crossing_index][edge_index] = self.pd_code[crossing_index][edge_index]
    
    pd_code = [tuple(crossing) for crossing in pd_code]

    return Diagram(pd_code)
