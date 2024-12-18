from collections import deque
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
def bfs(grid: set[Position], start: Position, end: Position) -> int | None:
    nodes = deque([(start, 0)])
    visited = {start}
    while nodes:
        node, cost = nodes.pop()
        if node == end:
            return cost
        x, y = node
        for dx, dy in NEIGHBOURS:
            neighbour = (x + dx, y + dy)
            if neighbour in grid and neighbour not in visited:
                visited.add(neighbour)
                nodes.appendleft((neighbour, cost + 1))

size, n = 70, 1024
#size, n = 6, 12
start = 0, 0
end = size, size

full_grid = set(itertools.product(range(size+1), range(size+1)))
corrupted = list(parse(sys.stdin))
grid = full_grid - set(corrupted[:n])

# silver
print(bfs(grid, start, end))

# gold
grid = full_grid
for p in corrupted:
    grid.remove(p)
    cost = bfs(grid, start, end)
    if cost is None:
        print(p)
        break
