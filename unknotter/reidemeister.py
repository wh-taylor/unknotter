import math
import random
import time
from unknotter.diagram import *
from unknotter.properties import get_edges, _is_valid

def _is_unpokable(self: Diagram, edge1: Edge, edge2: Edge) -> bool:
    return any((
        self._is_open(edge1) and self._is_closed(edge2),
        self._is_open(edge2) and self._is_closed(edge1),
    ))

def _is_slidable(self: Diagram, edge1: Edge, edge2: Edge, edge3: Edge) -> bool:
    return any((
        self._is_open(edge1) and self._is_closed(edge2) and self._is_half_open(edge3),
        self._is_open(edge1) and self._is_closed(edge3) and self._is_half_open(edge2),
        self._is_open(edge2) and self._is_closed(edge1) and self._is_half_open(edge3),
        self._is_open(edge2) and self._is_closed(edge3) and self._is_half_open(edge1),
        self._is_open(edge3) and self._is_closed(edge1) and self._is_half_open(edge2),
        self._is_open(edge3) and self._is_closed(edge2) and self._is_half_open(edge1),
    ))

def get_twistables(self: Diagram) -> list[Edge]:
    """Return the list of edges that can be twisted (which is all of them)."""
    return get_edges(self)

def get_untwistables(self: Diagram) -> list[Edge]:
    """Return the list of edges that can be untwisted."""
    untwistables = []
    for crossing in self.pd_code:
        if len(set(crossing)) == 3:
            untwistables.append(max(set(crossing), key=crossing.count))
    return untwistables

def get_pokables(self: Diagram) -> list[tuple[Edge, Edge]]:
    """Return the list of ordered pairs of edges that can be poked."""
    pokables = []
    for edge in get_edges(self):
        pokable_with = []
        face_ccw, face_cw = self._get_adjacent_faces(edge)
        for signed_edge in face_ccw + face_cw:
            adj_edge = abs(signed_edge)
            if adj_edge != edge and adj_edge not in pokable_with:
                pokable_with.append(adj_edge)
        pokables += ((edge, e) for e in pokable_with)
    return pokables

def get_unpokables(self: Diagram) -> list[tuple[Edge, Edge]]:
    """Return the list of ordered pairs of edges that can be unpoked."""
    unpokables = []
    for edge in get_edges(self):
        if any(edge in pair for pair in unpokables):
            continue
        face_ccw, face_cw = self._get_adjacent_faces(edge)
        if len(face_ccw) == 2 and _is_unpokable(self, *[abs(n) for n in face_ccw]):
                unpokables.append(tuple(sorted(abs(n) for n in face_ccw)))
        if len(face_cw) == 2 and _is_unpokable(self, *[abs(n) for n in face_cw]):
                unpokables.append(tuple(sorted(abs(n) for n in face_cw)))
    return unpokables

def get_slidables(self: Diagram) -> list[tuple[Edge, Edge, Edge]]:
    """Return the list of ordered triplets of edges that can be slid."""
    slidables = []
    for edge in get_edges(self):
        if any(edge in triplet for triplet in slidables):
            continue
        face_ccw, face_cw = self._get_adjacent_faces(edge)
        if len(face_ccw) == 3 and _is_slidable(self, *[abs(n) for n in face_ccw]):
                slidables.append(tuple(sorted(abs(n) for n in face_ccw)))
        if len(face_cw) == 3 and _is_slidable(self, *[abs(n) for n in face_cw]):
                slidables.append(tuple(sorted(abs(n) for n in face_cw)))
    return slidables

def _prepare_twist(self: Diagram, target_edge: Edge) -> PDNotation:
    """Readjust the edge values of `diagram` with the expectation of a twist at `target_edge`."""
    pd_code: PDNotation = []

    # Map over each edge in each crossing of `diagram`.
    for crossing in self.pd_code:
        new_crossing_as_list: list[Edge] = []
        # If the target edge lies on a twist
        if crossing.count(target_edge) == 2:
            if self._next(crossing[0]) == crossing[1] or self._next(self._next(crossing[0])) == crossing[1]:
                new_crossing_as_list.append(crossing[0])
                new_crossing_as_list.append(crossing[1] + 2)
                new_crossing_as_list.append(crossing[2])
                new_crossing_as_list.append(crossing[3] + 2)
            else:
                new_crossing_as_list.append(crossing[0] + 2)
                new_crossing_as_list.append(crossing[1])
                new_crossing_as_list.append(crossing[2] + 2)
                new_crossing_as_list.append(crossing[3])
        else:
            for edge in crossing:
                # If a given edge comes before the target edge, leave it alone.
                # If a given edge comes after the target edge, add two.
                # If it is the target edge, leave it alone if it connects with the
                #   previous edge or add two if it connects with the next edge.
                if edge < target_edge or edge == target_edge and self._prev(edge) in crossing:
                    new_crossing_as_list.append(edge)
                else:
                    new_crossing_as_list.append(edge + 2)
        new_crossing: Crossing = tuple(new_crossing_as_list)
        pd_code.append(new_crossing)
    
    return pd_code

def left_positive_twist(self: Diagram, edge: Edge) -> Diagram:
    """Apply a left-positive twist on `edge`."""
    pd_code = _prepare_twist(self, edge)
    pd_code.append((edge, edge + 2, edge + 1, edge + 1))
    return Diagram(pd_code)

def left_negative_twist(self: Diagram, edge: Edge) -> Diagram:
    """Apply a left-negative twist on `edge`."""
    pd_code = _prepare_twist(self, edge)
    pd_code.append((edge + 1, edge, edge + 2, edge + 1))
    return Diagram(pd_code)

def right_positive_twist(self: Diagram, edge: Edge) -> Diagram:
    """Apply a right-positive twist on `edge`."""
    pd_code = _prepare_twist(self, edge)
    pd_code.append((edge + 1, edge + 1, edge + 2, edge))
    return Diagram(pd_code)

def right_negative_twist(self: Diagram, edge: Edge) -> Diagram:
    """Apply a right-negative twist on `edge`."""
    pd_code = _prepare_twist(self, edge)
    pd_code.append((edge, edge + 1, edge + 1, edge + 2))
    return Diagram(pd_code)

def untwist(self: Diagram, edge: Edge) -> Diagram:
    """Remove the twist adjacent to the given edge."""
    if edge == 1 or edge == 2*len(self.pd_code):
        return untwist(self.shift(1), self._next(edge))
    pd_code: PDNotation = self.pd_code.copy()
    for i, crossing in enumerate(pd_code):
        if crossing.count(edge) == 2:
            del pd_code[i]
            break
    else:
        raise ReidemeisterError("given edge is not on a twist, so it cannot be untwisted.")
    pd_code = [tuple(e - 2 if e > edge else e for e in crossing) for crossing in pd_code]
    return Diagram(pd_code)

def _prepare_poke(self: Diagram, lower_edge: Edge, higher_edge: Edge) -> PDNotation:
    """Readjust the edge values of `diagram` with the expectation of a poke between the two edges."""
    pd_code: PDNotation = []

    # Map over each edge in each crossing of `diagram`.
    for crossing in self.pd_code:
        new_crossing_as_list: list[Edge] = []
        if crossing.count(lower_edge) == 2 or crossing.count(higher_edge) == 2:
            raise NotImplementedError
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
                edge == lower_edge and self._prev(edge) in crossing)
            should_add_two = (
                edge == lower_edge or
                lower_edge < edge < higher_edge or
                edge == higher_edge and self._prev(edge) in crossing)

            if should_add_none:
                new_crossing_as_list.append(edge)
            elif should_add_two:
                new_crossing_as_list.append(edge + 2)
            else:
                new_crossing_as_list.append(edge + 4)
        new_crossing: Crossing = tuple(new_crossing_as_list)
        pd_code.append(new_crossing)

    return pd_code

def poke(self: Diagram, under_edge: Edge, over_edge: Edge) -> Diagram:
    """Poke `under_edge` underneath `over_edge`."""
    # if under_edge == 1 or over_edge == 1 or under_edge == 2*len(self.pd_code) or over_edge == 2*len(self.pd_code):
    #     return poke(self.shift(1), self._next(under_edge), self._next(over_edge))

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

    face_ccw, face_cw = self._get_adjacent_faces(lower_edge)

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

def unpoke(self: Diagram, edge1: Edge, edge2: Edge) -> Diagram:
    """Remove the poke between the two given edges."""
    # if edge1 == 1 or edge2 == 1 or edge1 == 2*len(self.pd_code) or edge2 == 2*len(self.pd_code):
    #     return unpoke(self.shift(1), self._next(edge1), self._next(edge2))
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

def slide(self: Diagram, edge1: Edge, edge2: Edge, edge3: Edge) -> Diagram:
    """Slide an edge over the face formed by the three given edges."""
    edges = [edge1, edge2, edge3]

    # Check if edges all lie on the same face
    face_ccw, face_cw = self._get_adjacent_faces(edge1)
    if not (all(edge in face_ccw or -edge in face_ccw for edge in edges) and len(face_ccw) == 3 or all(edge in face_cw or -edge in face_cw for edge in edges) and len(face_cw) == 3):
        raise ReidemeisterError("can only slide three edges along the same face.")
    
    # Check if edges are layered properly
    if not _is_slidable(self, edge1, edge2, edge3):
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
                friend_crossing_index, friend_edge_index = self._get_friend_index(crossing_index, edge_index)
                pd_code[crossing_index][edge_index] = (
                    self.pd_code[friend_crossing_index][(friend_edge_index + 2) % 4]
                )
            elif any(edge in self.pd_code[crossing_index] for edge in edges):
                pd_code[crossing_index][edge_index] = self.pd_code[crossing_index][(edge_index + 2) % 4]
            else:
                pd_code[crossing_index][edge_index] = self.pd_code[crossing_index][edge_index]
    
    pd_code = [tuple(crossing) for crossing in pd_code]

    return Diagram(pd_code)

def apply_random_move(self: Diagram, beta: float) -> Diagram:
    numerical_weights: list[float] = [
        math.e**-beta,
        math.e**beta,
        math.e**(-2*beta),
        math.e**(2*beta),
        1
    ]

    twistables = get_twistables(self)
    untwistables = get_untwistables(self)
    pokables = get_pokables(self)
    unpokables = get_unpokables(self)
    slidables = get_slidables(self)

    options = [twistables, untwistables, pokables, unpokables, slidables]

    weights = [0 if len(l) == 0 else w for w, l in zip(numerical_weights, options)]

    move_decision = random.choices([1, 2, 3, 4, 5], weights=weights)[0]

    try:
        match move_decision:
            case 1:
                edge = random.choices(twistables)[0]
                twist_decision = random.choices([1, 2, 3, 4])[0]
                match twist_decision:
                    case 1:
                        return left_positive_twist(self, edge)
                    case 2:
                        return left_negative_twist(self, edge)
                    case 3:
                        return right_positive_twist(self, edge)
                    case 4:
                        return right_negative_twist(self, edge)
            case 2:
                edge = random.choices(untwistables)[0]
                return untwist(self, edge)
            case 3:
                edges = random.choices(pokables)[0]
                return poke(self, *edges)
            case 4:
                edges = random.choices(unpokables)[0]
                return unpoke(self, *edges)
            case 5:
                edges = random.choices(slidables)[0]
                return slide(self, *edges)
    except NotImplementedError:
        return apply_random_move(self, beta)

def randomeister(self: Diagram, moves: int, beta: float) -> list[Diagram]:
    diagrams: list[Diagram] = [self]
    diagram = self
    for _ in range(moves):
        diagram = apply_random_move(diagram, beta)
        diagrams.append(diagram)
    return diagrams

def unknot_solver(self: Diagram, beta: float):
    diagram = self
    i = 0
    t0 = time.time()
    while len(diagram.pd_code) > 2:
        diagram = apply_random_move(diagram, beta)
        # print(len(diagram.pd_code), end=', ')
        assert _is_valid(diagram)
        i += 1

        if i > 2000:
            print('Iterations exceeded 2000; given diagram is most likely not an unknot.')
            t1 = time.time()
            print('Time:', t1 - t0)
            return
    t1 = time.time()
    print('Iterations:', i)
    print('Time:', t1 - t0)
