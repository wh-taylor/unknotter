from __future__ import annotations

Edge = int
Crossing = tuple[Edge, Edge, Edge, Edge]
PDNotation = list[Crossing]

class Diagram:
    def __init__(self, pd_code):
        self.pd_code: PDNotation = pd_code
    
    def __repr__(self) -> Diagram:
        return 'PD [ ' + ',\n     '.join('(' + ', '.join(str(e) for e in crossing) + ')' for crossing in self.pd_code) + ' ]'
    
    # Get a list of all crossings that are adjacent to a given edge.
    def _get_crossings_with_edge(self, edge: Edge) -> list[Crossing]:
        return [crossing for crossing in self.pd_code if edge in crossing]
    
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
        raise NotImplemented

    # Return the Dowker-Thistlethwait notation of a diagram.
    def get_dt_notation(self) -> list[int]:
        raise NotImplemented
    
    def _shift_edge(edge: Edge, n: int, mod: int) -> Edge:
        return (edge + n - 1) % mod + 1

    # Return a diagram with all of its edge values shifted up by `n`.
    def shift(self, n: int) -> Diagram:
        mod = 2 * len(self.pd_code)
        return Diagram([tuple(Diagram._shift_edge(edge, n, mod) for edge in crossing) for crossing in self.pd_code])

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
        return all(self.pd_code[i][j] == other.pd_code[i][j]
            for i in range(len(self.pd_code))
            for j in range(4))

    # Check if a diagram is equivalent to another considering orientation.
    def __eq__(self, diagram2: Diagram):
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
        raise NotImplemented

    # Return the joining of two diagrams by given edges (generalizes connected sum).
    def join(self, other: Diagram, self_edge: Edge, other_edge: Edge) -> Diagram:
        raise NotImplemented

    # Return the Jones polynomial of a diagram.
    def get_jones_polynomial(self):
        raise NotImplemented

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
                if edge < target_edge or edge == target_edge and edge - 1 in crossing:
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

    # Apply a negative twist on `target_edge`.
    def _negtwist(self, target_edge: Edge) -> Diagram:
        pd_code = self._prepare_twist(target_edge)
        pd_code.append((target_edge, target_edge + 1, target_edge + 1, target_edge + 2))

    # Twist `target_edge`.
    def twist(self, target_edge: Edge, is_positive: bool = True) -> Diagram:
        return self._postwist(target_edge) if is_positive else self._negtwist(target_edge)

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
                    edge == lower_edge and edge - 1 in crossing)
                should_add_two = (
                    edge == lower_edge or
                    lower_edge < edge < higher_edge or
                    edge == higher_edge and edge - 1 in crossing)

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
    # TODO: raise an exception if a poke is not possible (not in one face).
    def poke(self, under_edge: Edge, over_edge: Edge) -> Diagram:
        lower_edge = min(under_edge, over_edge)
        higher_edge = max(under_edge, over_edge)

        pd_code: PDNotation = self._prepare_poke(lower_edge, higher_edge)
        
        # Add the two new crossings.
        if under_edge == lower_edge:
            pd_code.append((lower_edge, higher_edge + 2, lower_edge + 1, higher_edge + 3))
            pd_code.append((lower_edge + 1, higher_edge + 4, lower_edge + 2, higher_edge + 3))
        else:
            pd_code.append((higher_edge + 2, lower_edge + 1, higher_edge + 3, lower_edge))
            pd_code.append((higher_edge + 3, lower_edge + 1, higher_edge + 4, lower_edge + 2))

        return Diagram(pd_code)

    # Slide an edge over the face formed by the three given edges.
    # TODO: raise an exception if a slide is not possible (not in one face, incorrect crossing).
    def slide(self, edge1: Edge, edge2: Edge, edge3: Edge) -> Diagram:
        # Initialize three crossings to be updated while iterating over the relevant crossings.
        new_crossings_mutable = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        # Get the three crossings connecting the three edges.
        relevant_crossings = list(set(
            self._get_crossings_with_edge(edge1) +
            self._get_crossings_with_edge(edge2) +
            self._get_crossings_with_edge(edge3)))

        # Map over each edge in each relevant crossing by index.
        # The crossing index is the index of a crossing in the PD notation as a list.
        for crossing_index in range(3):
            # The edge index is the index of an edge in a crossing.
            for edge_index in range(4):
                # Shift the relevant crossings down two. However, if the edge is one of the three edges forming the face of the slide, use the edge shifted down two from its friend instead.
                # See `_get_friend_index` for the definition of a friend.
                if relevant_crossings[crossing_index][edge_index] in [edge1, edge2, edge3]:
                    friend_crossing_index, friend_edge_index = self._get_friend_index(crossing_index, edge_index)
                    new_crossings_mutable[crossing_index][edge_index] = (
                        relevant_crossings[friend_crossing_index][(friend_edge_index + 2) % 4])
                else:
                    new_crossings_mutable[crossing_index][edge_index] = (
                        relevant_crossings[crossing_index][(edge_index + 2) % 4])
        
        new_crossings = [tuple(crossing) for crossing in new_crossings_mutable]

        pd_code = [crossing for crossing in self.pd_code if crossing not in relevant_crossings] + new_crossings

        return Diagram(pd_code)
