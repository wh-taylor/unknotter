crossing = tuple[int, int, int, int]
pd_notation = list[crossing]



class KnotDiagram:
    def __init__(self, pd_code):
        self.pd_code: pd_notation = pd_code
    
    def __repr__(self):
        return 'PD { ' + ',\n     '.join('(' + ', '.join(str(e) for e in crossing) + ')' for crossing in self.pd_code) + ' }'

    def reverse(self):
        return KnotDiagram({(d, c, b, a) for (a, b, c, d) in self.pd_code})
    
    def reflect(self):
        return KnotDiagram({(a, d, c, b) for (a, b, c, d) in self.pd_code})
    
    def edge_map(self, f, new_crossings: list[crossing]):
        pd_code = {tuple(f(e, x) for e in x) for x in self.pd_code}
        for crossing in new_crossings: pd_code.add(crossing)
        return KnotDiagram(pd_code)

    def unchanged(self):
        return self.edge_map(
            lambda e, _: e,
            []
        )

    def add_negR1(self, edge: int):
        return self.edge_map(
            lambda e, x:
                e if e < edge else
                e if e == edge and e-1 in x else
                e+2,
            [(edge, edge+1, edge+1, edge+2)]
        )

    def add_posR1(self, edge: int):
        return self.edge_map(
            lambda e, x:
                e if e < edge else
                e if e == edge and e-1 in x else
                e+2,
            [(edge+1, edge+1, edge+2, edge)]
        )

    def add_underR2(self, edge1, edge2):
        a = min(edge1, edge2)
        b = max(edge1, edge2)
        return self.edge_map(
            lambda e, x:
                e if e < a else
                e if e == a and e-1 in x else
                e+2 if e == a and e+1 in x else
                e+2 if a < e and e < b else
                e+2 if e == b and e-1 in x else
                e+4 if e == b and e+1 in x else
                e+4,
            {
                (a, b+2, a+1, b+3),
                (a+1, b+4, a+2, b+3)
            }
        )

    def add_overR2(self, edge1, edge2):
        a = min(edge1, edge2)
        b = max(edge1, edge2)
        return self.edge_map(
            lambda e, x:
                e if e < a else
                e if e == a and e-1 in x else
                e+2 if e == a and e+1 in x else
                e+2 if a < e and e < b else
                e+2 if e == b and e-1 in x else
                e+4 if e == b and e+1 in x else
                e+4,
            {
                (b+2, a+1, b+3, a),
                (b+3, a+1, b+4, a+2)
            }
        )