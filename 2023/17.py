from collections import deque
import heapq
import sys
from typing import Dict, Iterable, List, Sequence, TextIO, Tuple

Position = Tuple[int, int]
Grid = Dict[Position, int]
DIRECTIONS = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
]

def parse(f: TextIO) -> Grid:
    grid: Grid = {}
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            grid[(x, y)] = int(c)
    return grid

def add(p: Position, d: Tuple[int, int]) -> Position:
    x, y = p
    dx, dy = d
    return x + dx, y + dy

def sub(a: Position, b: Position) -> Tuple[int, int]:
    ax, ay = a
    bx, by = b
    return ax - bx, ay - by

def is_legal(history: Tuple) -> bool:
    previous = (0, 0)
    count = 0
    for a, b in zip(history, history[1:]):
        delta = sub(a, b)
        if delta == previous:
            count += 1
            if count >= 3 - 1:
                return False
        else:
            count = 0
        previous = delta
    return True


def search(grid: Grid, start: Position, end: Position, n: int = 3) -> Sequence[Position]:
    # keep of best heat loss per position
    best = {}
    queue = deque([(end, 0, tuple())])
    while queue:
        p, heatloss, history = queue.popleft()
        if p not in grid:
            continue
        if not is_legal(history):
            continue
        if p == start:
            return list(reversed(history))
        b = best.get(p)
        if b is not None and b < heatloss:
            # we already found a better way
            continue
        best[p] = heatloss
        for d in DIRECTIONS:
            queue.append((add(p, d), heatloss + grid[p], history + (p,)))
    raise ValueError(f'No path from {start} to {end}')


def heatloss(grid: Grid, trail: Sequence[Position]) -> int:
    return sum(grid[p] for p in trail)

def print_grid(grid: Grid, trail: Sequence[Position] = ()) -> None:
    xmin, ymin = min(grid)
    xmax, ymax = max(grid)
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            p = x, y
            if p in trail:
                print('#', end='')
            else:
                print(grid.get(p, '.'), end='')
        print()
        

def dijkstra(grid: Grid, start: Position, end: Position):
    costs = {start: 0}  
    queue = [(0, start)]
    previous: Dict[Position, Position] = {}  # keep track of shortest path
    while queue:
        cost, p = heapq.heappop(queue)
        if p == end:
            print('ok. finding shortest path')
            path = []
            while p is not None:
                path.append(p)
                p = previous.get(p)
            path.reverse()
            return path
        # skip if we already found something better
        if cost > costs.get(p):
            continue
        for direction in DIRECTIONS:
            neighbor = add(p, direction)
            if neighbor not in grid:
                continue
            neighbor_cost = cost + grid[p]
            if neighbor not in costs or neighbor_cost < costs[neighbor]:
                heapq.heappush(queue, (neighbor_cost, neighbor))
                costs[neighbor] = neighbor_cost
                previous[neighbor] = p

grid = parse(sys.stdin)
start = min(grid)
end = max(grid)
#history = search(grid, start, end)

trail = dijkstra(grid, start, end)
print_grid(grid, trail=trail)
#print(heatloss(grid, trail=history))

