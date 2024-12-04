from __future__ import annotations
import sys

Grid = dict[tuple[int, int], str]

def to_grid(f) -> Grid:
    grid = {}
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            grid[(x, y)] = c
    return grid

DIRECTIONS = [
    (1, 0), # right
    (-1, 0), # left
    (0, -1), # up
    (0, 1), # down
    (1, 1), # right+down
    (1, -1), # right+up
    (-1, 1), # left+down
    (-1, -1), # left+up
]
def search1(grid: Grid, string: str) -> int:
    x0, y0 = min(grid)
    x1, y1 = max(grid)
    count = 0
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for dx, dy in DIRECTIONS:
                if all(grid.get((x + dx * i, y + dy * i)) == c  for i, c in enumerate(string)):
                    count += 1
    return count

def search2(grid: Grid) -> int:
    cross = (('M', 'S'), ('S', 'M'))
    x0, y0 = min(grid)
    x1, y1 = max(grid)
    count = 0
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            d1 = (grid.get((x - 1, y - 1)), grid.get((x + 1, y + 1)))
            d2 = (grid.get((x - 1, y + 1)), grid.get((x + 1, y - 1)))
            mid = grid.get((x, y))
            if d1 in cross and d2 in cross and mid == 'A':
                count += 1
    return count

grid = to_grid(sys.stdin)
print(search1(grid, 'XMAS'))
print(search2(grid))