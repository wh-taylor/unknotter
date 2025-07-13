from unknotter.catalog import _raw_pd_to_pd
from unknotter.diagram import Diagram

def read_to_list(filename: str, count: int = -1):
    catalog: list[tuple[str, str]] = []
    with open(filename) as f:
        lines = f.readlines()[1:count+1] if count >= 0 else f.readlines()[1:]
        for line in lines:
            parts = line.split(',')
            name, raw_pd = parts[0], parts[1]
            catalog.append((name, _raw_pd_to_pd(raw_pd)))
    return catalog

