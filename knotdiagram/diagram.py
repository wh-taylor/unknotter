from __future__ import annotations
from itertools import product
from math import prod
from polynomial import *

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
    
    # Get a list of all crossings that are adjacent to a given edge.
    def _get_crossings_with_edge(self, edge: Edge) -> list[Crossing]:
        return [crossing for crossing in self.pd_code if edge in crossing]
    
    # Shift an edge by a given amount, wrapping around the number of edges.
    def _shiftmod(self, edge: Edge, n: int) -> Edge:
        return (edge + n - 1) % (2*len(self.pd_code)) + 1
    
    # Get the edge after a given edge (+1 with wraparound).
    def _next(self, edge: Edge) -> Edge:
        return self._shiftmod(edge, 1)
    
    # Get the edge before a given edge (-1 with wraparound).
    def _prev(self, edge: Edge) -> Edge:
        return self._shiftmod(edge, -1)
    
    # Given the index of an edge, get the index of its friend.
    # Say we have two crossings: (_, _, _, 2), (_, _, 2, _).
    # The first 2 is in the first crossing in the fourth position, so it has the index (1, 4).
    # The second 2 is in the second crossing in the third position, so it has the index (2, 3).
    # Thus, diagram._get_friend_index(1, 4) = (2, 3) and diagram._get_friend_index(2, 3) = (1, 4).
    def _get_friend_index(self, crossing_index: int, edge_index: int) -> tuple[int, int]:
        edge = self.pd_code[crossing_index][edge_index]
        crossings_with_edge = self._get_crossings_with_edge(edge)
        
        if len(crossings_with_edge) == 1:
            pos = [i for i, row in enumerate(self.pd_code[crossing_index]) if row == edge]
            return (crossing_index, pos[1] if pos[0] == edge_index else pos[0])
        
        if crossings_with_edge[0] == self.pd_code[crossing_index]:
            return (next(i for i, row in enumerate(self.pd_code) if row == crossings_with_edge[1]), next(i for i, x in enumerate(crossings_with_edge[1]) if x == edge))

        return (next(i for i, row in enumerate(self.pd_code) if row == crossings_with_edge[0]), next(i for i, x in enumerate(crossings_with_edge[0]) if x == edge))
    
    # Return the Gauss code of a diagram.
    def get_gauss_code(self) -> list[int]:
        raise NotImplementedError

    # Return the Dowker-Thistlethwait notation of a diagram.
    def get_dt_notation(self) -> list[int]:
        raise NotImplementedError

    # Return a diagram with all of its edge values shifted up by `n`.
    def shift(self, n: int) -> Diagram:
        return Diagram([tuple(self._shiftmod(edge, n) for edge in crossing) for crossing in self.pd_code])

    # Return a diagram with all of its edge values shifted up by `n` without wrapping around.
    # This method is meant for adjusting a diagram to be combined with another.
    def _shift_unbounded(self, n: int) -> Diagram:
        return Diagram([tuple(edge + n for edge in crossing) for crossing in self.pd_code])

    # Return a diagram with opposite orientation of `diagram`.
    def reverse(self) -> Diagram:
        return Diagram([(d, c, b, a) for (a, b, c, d) in self.pd_code])

    # Return a diagram of the reflection of the link of `diagram`.
    def reflect(self) -> Diagram:
        return Diagram([(a, d, c, b) for (a, b, c, d) in self.pd_code])

    # Return an exact copy of `diagram`.
    def copy(self) -> Diagram:
        return Diagram(self.pd_code.copy())

    # Return true if and only if all edge values of both diagrams are completely identical.
    def identical(self, other: Diagram) -> bool:
        if len(self.pd_code) != len(other.pd_code): return False
        return set(self.pd_code) == set(other.pd_code)

    # Check if a diagram is equivalent to another considering orientation.
    def __eq__(self, diagram2: Diagram):
        if self.pd_code == diagram2.pd_code: return True
        for n in range(2*len(self.pd_code)):
            if self.shift(n).identical(diagram2):
                return True
        return False

    # Check if a diagram is equivalent to another up to orientation.
    # Two knows with reverse orientations are "congruent".
    def is_congruent(self, diagram2: Diagram):
        for n in range(2*len(self.pd_code)):
            if self.shift(n).identical(diagram2) or self.reverse().shift(n).identical(diagram2):
                return True
        return False

    # Return the disjoint union of two diagrams.
    def disjoint_union(self) -> Diagram:
        raise NotImplementedError

    # Return the joining of two diagrams by given edges (generalizes connected sum).
    def join(self, other: Diagram, self_edge: Edge, other_edge: Edge) -> Diagram:
        raise NotImplementedError

    # Return the Kauffman bracket of a diagram.
    def get_kauffman_bracket(self) -> KnotPoly:
        if self == Diagram([]): return KnotPoly({0: 1})

        factored_poly = [(((a, d), (b, c)), ((a, b), (c, d))) for a, b, c, d in self.pd_code]

        distributed_poly = [(sum(1-2*i for i in ii), [factor for term in terms for factor in term]) for ii, terms in zip(product(*(range(2) for _ in factored_poly)), product(*factored_poly))]

        for power, term in distributed_poly:
            matched_at_all = True
            while matched_at_all:
                matched_at_all = False
                i = 0
                if len(term) == 1: break
                while i < len(term):
                    j = i + 1
                    while j < len(term):
                        x1, x2 = term[i], term[j]
                        a1, b1 = x1
                        a2, b2 = x2

                        matched = True

                        if a1 == b2 and a2 == b1 or a1 == a2 and b1 == b2:
                            term.append((a1, a1))
                        elif a1 == a2:
                            term.append((b1, b2))
                        elif a1 == b2:
                            term.append((b1, a2))
                        elif b1 == a2:
                            term.append((a1, b2))
                        elif b1 == b2:
                            term.append((a1, a2))
                        else:
                            matched = False

                        if matched: del term[j], term[i]
                        if matched: matched_at_all = True
                        j += 1
                    i += 1

        newlist = [(power, len(term)-1) for power, term in distributed_poly]

        disjoint_unknot_poly = KnotPoly({2: -1, -2: -1})

        return sum((KnotPoly({power1: 1}) * disjoint_unknot_poly**power2 for power1, power2 in newlist), KnotPoly.zero())
    
    def get_writhe(self) -> int:
        writhe = 0
        for _, b, _, d in self.pd_code:
            if self._next(b) == d:
                writhe -= 1
            else:
                writhe += 1
        return writhe

    # Return the Jones polynomial of a diagram.
    def get_jones_polynomial(self) -> KnotPoly:
        writhe = self.get_writhe()
        kauffman_bracket = self.get_kauffman_bracket()
        raw_jones_polynomial = kauffman_bracket * KnotPoly({3*writhe: 1 if writhe % 2 == 0 else -1})
        coefficients = {powers[0]/4: coefficients for powers, coefficients in raw_jones_polynomial.coefficients.items()}
        return KnotPoly(coefficients)
    
    # Return the list of edges.
    def get_edges(self) -> list[Edge]:
        return [i + 1 for i in range(2 * len(self.pd_code))]
    
    # Return the list of edges that can be twisted (which is all of them).
    def get_twistables(self) -> list[Edge]:
        return self.get_edges()
    
    # Return the list of edges that can be untwisted.
    def get_untwistables(self) -> list[Edge]:
        untwistables = []
        for crossing in self.pd_code:
            if len(set(crossing)) == 3:
                untwistables.append(max(set(crossing), key=crossing.count))
        return untwistables
    
    # Return the list of (ordered) pairs of edges that can be poked.
    def get_pokables(self) -> list[tuple[Edge, Edge]]:
        pokables = []
        for edge in self.get_edges():
            pokable_with = []
            face_ccw, face_cw = self.get_adjacent_faces(edge)
            for signed_edge in face_ccw + face_cw:
                adj_edge = abs(signed_edge)
                if adj_edge != edge and adj_edge not in pokable_with:
                    pokable_with.append(adj_edge)
            pokables += ((edge, e) for e in pokable_with)
        return pokables
    
    # Return the list of (ordered) pairs of edges that can be unpoked.
    def get_unpokables(self) -> list[tuple[Edge, Edge]]:
        unpokables = []
        for edge in self.get_edges():
            if any(edge in pair for pair in unpokables):
                continue
            face_ccw, face_cw = self.get_adjacent_faces(edge)
            if len(face_ccw) == 2 and self.is_unpokable(*[abs(n) for n in face_ccw]):
                    unpokables.append(tuple(sorted(abs(n) for n in face_ccw)))
            if len(face_cw) == 2 and self.is_unpokable(*[abs(n) for n in face_cw]):
                    unpokables.append(tuple(sorted(abs(n) for n in face_cw)))
        return unpokables
    
    # Return the list of (ordered) triplets of edges that can be slid.
    def get_slidables(self) -> list[tuple[Edge, Edge, Edge]]:
        slidables = []
        for edge in self.get_edges():
            if any(edge in triplet for triplet in slidables):
                continue
            face_ccw, face_cw = self.get_adjacent_faces(edge)
            if len(face_ccw) == 3 and self.is_slidable(*[abs(n) for n in face_ccw]):
                    slidables.append(tuple(sorted(abs(n) for n in face_ccw)))
            if len(face_cw) == 3 and self.is_slidable(*[abs(n) for n in face_cw]):
                    slidables.append(tuple(sorted(abs(n) for n in face_cw)))
        return slidables

    # Readjust the edge values of `diagram` with the expectation of a twist at `target_edge`.
    def _prepare_twist(self, target_edge: Edge) -> PDNotation:
        pd_code: PDNotation = []

        # Map over each edge in each crossing of `diagram`.
        for crossing in self.pd_code:
            new_crossing_as_list: list[Edge] = []
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

    # Apply a positive twist on `target_edge`.
    def _postwist(self, target_edge: Edge) -> Diagram:
        pd_code = self._prepare_twist(target_edge)
        pd_code.append((target_edge + 1, target_edge + 1, target_edge + 2, target_edge))
        return Diagram(pd_code)

    # Apply a negative twist on `target_edge`.
    def _negtwist(self, target_edge: Edge) -> Diagram:
        pd_code = self._prepare_twist(target_edge)
        pd_code.append((target_edge, target_edge + 1, target_edge + 1, target_edge + 2))
        return Diagram(pd_code)

    # Twist `target_edge`.
    def twist(self, target_edge: Edge, is_positive: bool = True) -> Diagram:
        return self._postwist(target_edge) if is_positive else self._negtwist(target_edge)
    
    # Remove the twist adjacent to the given edge.
    def untwist(self, edge: Edge) -> Diagram:
        pd_code: PDNotation = self.pd_code.copy()
        for i, crossing in enumerate(pd_code):
            if crossing.count(edge) == 2:
                del pd_code[i]
                break
        else:
            raise ReidemeisterError("given edge is not on a twist, so it cannot be untwisted.")
        pd_code = [tuple(e - 2 if e > edge else e for e in crossing) for crossing in pd_code]
        return Diagram(pd_code)
    
    # Returns whether or not the given index represents an edge that is facing its crossing.
    def index_is_facing(self, crossing_index: int, edge_index: int) -> bool:
        if edge_index == 0: return True
        if edge_index == 1:
            return self.pd_code[crossing_index][3] == self._next(self.pd_code[crossing_index][1])
        if edge_index == 3:
            return self.pd_code[crossing_index][1] == self._next(self.pd_code[crossing_index][3])

    # Get the index of the given edge in the crossing it faces toward.
    # Note: the edge index is never 2, since the edge would then be
    # facing away from the crossing.
    def get_forth_index(self, edge: Edge) -> tuple[int, int]:
        for crossing_index, crossing in enumerate(self.pd_code):
            if crossing[0] == edge:
                return crossing_index, 0
            if crossing[1] == edge and crossing[3] == self._next(edge):
                return crossing_index, 1
            if crossing[3] == edge and crossing[1] == self._next(edge):
                return crossing_index, 3
        raise NotImplementedError
    
    # Get the two faces adjacent to the given edge.
    # Following the direction the given edge is pointing, two faces can be extracted.
    # One by only going counterclockwise and one by only going clockwise.
    # Each face is given as a list of edges that are signed. Since we generate faces
    # based on a specific direction, the edge is negative if it goes against the direction
    # of the path we follow in generating the face.
    def get_adjacent_faces(self, edge: Edge) -> tuple[list[SignedEdge], list[SignedEdge]]:
        face_ccw: list[SignedEdge] = [edge]
        face_cw: list[SignedEdge] = [edge]

        # Generate the counterclockwise face.
        crossing_index, edge_index = self.get_forth_index(edge)
        edge_index = (edge_index - 1) % 4
        while self.pd_code[crossing_index][edge_index] != edge:
            sign = -1 if self.index_is_facing(crossing_index, edge_index) else 1
            face_ccw.append(sign * self.pd_code[crossing_index][edge_index])
            crossing_index, edge_index = self._get_friend_index(crossing_index, edge_index)
            edge_index = (edge_index - 1) % 4
        
        # Generate the clockwise face.
        crossing_index, edge_index = self.get_forth_index(edge)
        edge_index = (edge_index + 1) % 4
        while self.pd_code[crossing_index][edge_index] != edge:
            sign = -1 if self.index_is_facing(crossing_index, edge_index) else 1
            face_cw.append(sign * self.pd_code[crossing_index][edge_index])
            crossing_index, edge_index = self._get_friend_index(crossing_index, edge_index)
            edge_index = (edge_index + 1) % 4

        return (face_ccw, face_cw)

    # Readjust the edge values of `diagram` with the expectation of a poke between the two edges.
    def _prepare_poke(self, lower_edge: Edge, higher_edge: Edge) -> PDNotation:
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

    # Poke `under_edge` underneath `over_edge`.
    def poke(self, under_edge: Edge, over_edge: Edge) -> Diagram:
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

        face_ccw, face_cw = self.get_adjacent_faces(lower_edge)

        if not (higher_edge in face_cw or -higher_edge in face_cw or higher_edge in face_ccw or -higher_edge in face_ccw):
            raise ReidemeisterError("can only poke edges along the same face.")

        pd_code = self._prepare_poke(lower_edge, higher_edge)
        
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
    def unpoke(self, edge1: Edge, edge2: Edge) -> Diagram:
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
    
    # An edge is closed if, on both of the crossings it connects to, it crosses underneath.
    def is_closed(self, edge: Edge) -> bool:
        adj_crossings = [crossing for crossing in self.pd_code if edge in crossing]
        return edge in [adj_crossings[0][0], adj_crossings[0][2]] and edge in [adj_crossings[1][0], adj_crossings[1][2]]
    
    # An edge is open if, on both of the crossings it connects to, it crosses over.
    def is_open(self, edge: Edge) -> bool:
        adj_crossings = [crossing for crossing in self.pd_code if edge in crossing]
        return (edge in [adj_crossings[0][1], adj_crossings[0][3]]) and (edge in [adj_crossings[1][1], adj_crossings[1][3]])
    
    # An edge is half-open if it crosses over one of its crossings and under the other.
    def is_half_open(self, edge: Edge) -> bool:
        return not self.is_open(edge) and not self.is_closed(edge)
    
    def is_unpokable(self, edge1: Edge, edge2: Edge) -> bool:
        return any((
            self.is_open(edge1) and self.is_closed(edge2),
            self.is_open(edge2) and self.is_closed(edge1),
        ))

    def is_slidable(self, edge1: Edge, edge2: Edge, edge3: Edge) -> bool:
        return any((
            self.is_open(edge1) and self.is_closed(edge2) and self.is_half_open(edge3),
            self.is_open(edge1) and self.is_closed(edge3) and self.is_half_open(edge2),
            self.is_open(edge2) and self.is_closed(edge1) and self.is_half_open(edge3),
            self.is_open(edge2) and self.is_closed(edge3) and self.is_half_open(edge1),
            self.is_open(edge3) and self.is_closed(edge1) and self.is_half_open(edge2),
            self.is_open(edge3) and self.is_closed(edge2) and self.is_half_open(edge1),
        ))

    # Slide an edge over the face formed by the three given edges.
    def slide(self, edge1: Edge, edge2: Edge, edge3: Edge) -> Diagram:
        edges = [edge1, edge2, edge3]

        # Check if edges all lie on the same face
        face_ccw, face_cw = self.get_adjacent_faces(edge1)
        if not (all(edge in face_ccw or -edge in face_ccw for edge in edges) and len(face_ccw) == 3 or all(edge in face_cw or -edge in face_cw for edge in edges) and len(face_cw) == 3):
            raise ReidemeisterError("can only slide three edges along the same face.")
        
        # Check if edges are layered properly
        if not self.is_slidable(edge1, edge2, edge3):
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
