from collections import deque
import heapq
import sys
from typing import Dict, Iterable, List, Optional, Sequence, TextIO, Tuple

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
        

def trail_for(p: Position, previous: Dict[Position, Position], n: Optional[int] = None) -> List[Tuple[int, int]]:
    d = []
    i = 0
    while p is not None and (n is None or i < n):
        d.append(p)
        i += 1
        p = previous.get(p)
    return d

def deltas(trail: Sequence[Position]) -> Iterable[Tuple[int, int]]:
    for a, b in zip(trail, trail[1:]):
        yield sub(a, b)

def dijkstra(grid: Grid, start: Position, end: Position):
    costs = {start: 0}  
    queue = [(0, start)]
    previous: Dict[Position, Position] = {}  # keep track of shortest path
    while queue:
        cost, p = heapq.heappop(queue)
        if p == end:
            return trail_for(p, previous)
        # skip if we already found something better
        if cost > costs.get(p):
            continue
        neighbor_cost = cost + grid[p]
        ds = list(deltas(trail_for(p, previous, 4)))
        for direction in DIRECTIONS:
            neighbor = add(p, direction)
            if neighbor not in grid:
                continue
            # avoid path with 4 straight deltas
            if len(ds) == 3 and all(d == direction for d in ds):
                continue

            if neighbor not in costs or neighbor_cost < costs[neighbor]:
                heapq.heappush(queue, (neighbor_cost, neighbor))
                costs[neighbor] = neighbor_cost
                previous[neighbor] = p
    raise ValueError(f"No path from {start} to {end}")

grid = parse(sys.stdin)
start = min(grid)
end = max(grid)
#history = search(grid, start, end)

trail = dijkstra(grid, start, end)
print_grid(grid, trail=trail)
print(heatloss(grid, trail=trail))

