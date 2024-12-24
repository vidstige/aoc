from collections import defaultdict
import sys
from typing import Iterable, TextIO


Graph = dict[str, list[str]]
 

def parse(f: TextIO) -> Graph:
    graph = defaultdict(set)
    for line in f:
        a, b = line.rstrip().split('-')
        graph[a].add(b)
        graph[b].add(a)
    return dict(graph)

# 1 - all nodes
# 2 - all nodes + neighbors
# 3 - all nodes + neighbors + 
def fully_connected(graph: Graph, n: int):
    subgraphs = [{node} for node in graph]  # 0
    while not all(len(g) == 3 for g in subgraphs):
        nodes = subgraphs.pop(0)
        intersection = set.intersection(*(graph[node] for node in nodes))
        for i in intersection:
            subgraphs.append(nodes | {i})

    # convert to set of tuples
    tmp = {tuple(sorted(g)) for g in subgraphs}
    subgraphs = [set(g) for g in tmp]
    return subgraphs

graph = parse(sys.stdin)
subgraphs = fully_connected(graph, n=3)
for g in subgraphs:
    print(g, any(node.startswith('t') for node in g))

t = sum(1 for g in subgraphs if any(node.startswith('t') for node in g))

print(t)
