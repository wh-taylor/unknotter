from diagram import KnotDiagram

# Initialize pre-defined prime knot knot diagrams
knots = {}
with open('knotinfo.csv') as f:
    for line in f.readlines():
        parts = line.split(',')
        name, raw_pd = parts[0], parts[1]
        knots[name] = raw_pd

def knot(crossings, index, alt_status=''):
    name = f'{crossings}{alt_status}_{index}'
    raw_pd = knots[name]
    str_ns = raw_pd.replace('[', '') \
        .replace(']', '').strip().split(';')
    ns = list(map(int, str_ns))
    pd = set()
    for i in range(int(len(ns)/4)):
        pd.add(
            (ns[4*i], ns[4*i+1], ns[4*i+2], ns[4*i+3]))
    return KnotDiagram(pd)