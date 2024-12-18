import itertools
import sys
from typing import Iterable, TextIO

Position = tuple[int, int]

def parse(f: TextIO) -> Iterable[Position]:
    for line in f:
        x, y = line.split(',')
        yield  int(x), int (y)

NEIGHBOURS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]
def bfs(grid: set[Position], start: Position, end: Position):
    nodes = [(start, 0)]
    visited = {start}
    while nodes:
        node, cost = nodes.pop(0)
        if node == end:
            return cost
        x, y = node
        for dx, dy in NEIGHBOURS:
            neighbour = (x + dx, y + dy)
            if neighbour in grid and neighbour not in visited:
                visited.add(neighbour)
                nodes.append((neighbour, cost + 1))

full_grid = set(itertools.product(range(70+1), range(70+1)))

corrupted = parse(sys.stdin)
grid = full_grid - set(itertools.islice(corrupted, 1024))
m = bfs(grid, (0, 0), (70, 70))
print(m)
