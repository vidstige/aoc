import sys
from typing import Dict, List, TextIO, Tuple

Grid = Dict[Tuple[int, int], str]

def parse(f: TextIO) -> Grid:
    grid = {}
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            grid[(x, y)] = c
    return grid

def roll(grid: Grid) -> Grid:
    new = {}
    rolls = 0
    for (x, y), c in grid.items():
        if c == 'O' and grid.get((x, y - 1)) == '.':
            # roll up
            new[(x, y)] = '.'
            new[(x, y - 1)] = 'O'
            rolls += 1
        else:
            if (x, y) not in new:
                new[(x, y)] = c
    return new

def print_grid(grid: Grid) -> None:
    xmin, xmax = min(x for x, _ in grid), max(x for x, _ in grid) + 1
    ymin, ymax = min(y for _, y in grid), max(y for _, y in grid) + 1
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            print(grid.get((x, y), '?'), end='')
        print()

def load(grid: Grid) -> int:
    ymax = max(y for _, y in grid) + 1
    return sum(ymax - y for (_, y), c in grid.items() if c == 'O')

grid = parse(sys.stdin)
while True:
    new = roll(grid)
    if new == grid:
        break
    grid = new

print_grid(grid)
print(load(grid))