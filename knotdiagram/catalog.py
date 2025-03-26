from knotdiagram.diagram import Diagram, PDNotation
from itertools import islice

# Initialize pre-defined prime knot knot diagrams
_knot_catalog: dict[str, str] = {}
with open('knotdiagram/knotinfo.csv') as f:
    for line in f.readlines():
        parts = line.split(',')
        name, raw_pd = parts[0], parts[1]
        _knot_catalog[name] = raw_pd

def _raw_pd_to_pd(raw_pd: str) -> PDNotation:
    str_ns = raw_pd.replace('[', '').replace(']', '').strip().split(';')
    if str_ns == ['']: return [] # Handle the unknot (no crossings)
    ns = list(map(int, str_ns))
    pd_code = []
    for i in range(int(len(ns)/4)):
        pd_code.append(
            (ns[4*i], ns[4*i+1], ns[4*i+2], ns[4*i+3]))
    return pd_code

def knot(crossings: int, index: int, alt_status: str = '') -> Diagram:
    if alt_status == '' and crossings > 10:
        raise KeyError("knots with greater than 10 crossings require an argument 'a' or 'n'.")
    if alt_status != '' and crossings <= 10:
        raise KeyError("knots with crossings 10 or fewer are not distinguished by alternating or non-alternating.")

    name = f'{crossings}{alt_status}_{index}'
    
    try:
        raw_pd = _knot_catalog[name]
    except KeyError:
        raise KeyError(f"knot {name} does not exist.")

    return Diagram(_raw_pd_to_pd(raw_pd))

# Generator of all prime knot diagrams in the catalog.
KNOTS = ((name, Diagram(_raw_pd_to_pd(value))) for name, value in _knot_catalog.items())

def first_n_knots(n: int) -> list[tuple[str, Diagram]]:
    return islice(KNOTS, n)

# https://en.m.wikipedia.org/wiki/File:Thistlethwaite_unknot.svg
THISTLETHWAITE_UNKNOT = Diagram([
    (22, 2, 23, 1),   (3, 27, 4, 26),   (5, 21, 6, 20),
    (7, 18, 8, 19),   (9, 25, 10, 24),  (11, 2, 12, 3),
    (4, 13, 5, 14),   (15, 6, 16, 7),   (30, 17, 1, 18),
    (19, 14, 20, 15), (28, 22, 29, 21), (23, 11, 24, 10),
    (25, 9, 26, 8),   (27, 12, 28, 13), (16, 29, 17, 30)
])

# https://en.m.wikipedia.org/wiki/File:Ochiai_unknot.svg
OCHIAI_UNKNOT = Diagram([
    (12, 2, 13, 1),   (3, 6, 4, 7),     (5, 24, 6, 25),
    (7, 15, 8, 14),   (16, 10, 17, 9),  (26, 12, 1, 11),
    (13, 20, 14, 21), (22, 15, 23, 16), (10, 18, 11, 17),
    (19, 3, 20, 2),   (21, 8, 22, 9),   (23, 4, 24, 5),
    (25, 19, 26, 18)
])

# A simple unknot with a twist move.
INFINITY_UNKNOT = Diagram([(1, 1, 2, 2)])
