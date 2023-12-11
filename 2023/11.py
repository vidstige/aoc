from itertools import combinations
import sys
from typing import Set, TextIO, Tuple


Position = Tuple[int, int]
Grid = Set[Position]


def parse(f: TextIO) -> Grid:
    grid = set()
    for y, line in enumerate(f):
        for x, c in enumerate(line):
            if c == '#':
                grid.add((x, y))
    return grid


def bbox(grid: Grid) -> Tuple[Position, Position]:
    xs = [x for x, _ in grid]
    ys = [y for _, y in grid]
    return (min(xs), min(ys)), (max(xs), max(ys))


def expand_space(space: Grid) -> Tuple[Set[int], Set[int]]:
    (xmin, ymin), (xmax, ymax) = bbox(space)
    xs = set(x for x, _ in space)
    ys = set(y for _, y in space)
    ex = {x for x in range(xmin, xmax) if x not in xs}
    ey = {y for y in range(ymin, ymax) if y not in ys}
    return ex, ey


def expand(r: range, e: Set[int], m: int) -> int:
    return sum(m for cordinate in e if cordinate in r)


def manhattan(a: Position, b: Position, ex: Set[int], ey: Set[int], m: int) -> int:
    ax, ay = a
    bx, by = b
    xr = range(min(ax, bx), max(ax, bx))
    yr = range(min(ay, by), max(ay, by))
    return len(xr) + len(yr) + expand(xr, ex, m) + expand(yr, ey, m)


space = parse(sys.stdin)
ex, ey = expand_space(space)
# first star
print(sum(manhattan(a, b, ex, ey, m=2-1) for a, b in combinations(space, r=2)))
# second star
print(sum(manhattan(a, b, ex, ey, m=1000000-1) for a, b in combinations(space, r=2)))
