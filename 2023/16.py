import sys
from typing import Dict, Iterable, TextIO, Tuple

Position = Tuple[int, int]
Grid = Dict[Position, str]
RIGHT = (1, 0)
LEFT = (-1, 0)
DOWN = (0, 1)
UP = (0, -1)


def parse(f: TextIO) -> Grid:
    grid = {}
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            grid[(x, y)] = c
    return grid

def step(p: Position, direction: Tuple[int, int]) -> Position:
    x, y = p
    dx, dy = direction
    return x + dx, y + dy

def spread(grid: Grid, start: Position, direction: Tuple[int, int]) -> Iterable[Position]:
    stack = [(start, direction)]
    visited = set()  # keep track of where we've been
    while stack:
        p, d = stack.pop()
        if p not in grid:
            # we've moved out of the grid
            continue
        if (p, d) in visited:
            # we've already been this position and direction
            continue
        visited.add((p, d))
        yield p
        #print(grid[p])
        if grid[p] == '.':
            # empty space, just keep moving
            pass
        # split beam
        if grid[p] == '|':
            if d in (RIGHT, LEFT):
                stack.append((p, UP))
                stack.append((p, DOWN))
                continue
        if grid[p] == '-':
            if d in (UP, DOWN):
                stack.append((p, LEFT))
                stack.append((p, RIGHT))
                continue
        if grid[p] == '\\':
            dx, dy = d
            d = dy, dx
        if grid[p] == '/':
            dx, dy = d
            d = -dy, -dx
        stack.append((step(p, d), d))


grid = parse(sys.stdin)
energized = set()
for p in spread(grid, (0, 0), RIGHT):
    energized.add(p)

print(len(energized))
