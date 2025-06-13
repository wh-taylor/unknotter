from unknotter.catalog import _raw_pd_to_pd
from unknotter.diagram import Diagram

def read_to_list(filename: str):
    catalog: list[tuple[str, str]] = []
    with open(filename) as f:
        for line in f.readlines()[1:]:
            parts = line.split(',')
            name, raw_pd = parts[0], parts[1]
            catalog.append((name, Diagram(_raw_pd_to_pd(raw_pd))))
    return catalog

