from enum import Enum
import sys
from typing import Dict, Optional, TextIO, Tuple


class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

Pipe = Tuple[Direction, Direction]
Grid = Dict[Tuple[int, int], Pipe]


def parse_pipe(c: str) -> Optional[Pipe]:
    return {
        '|': (Direction.UP, Direction.DOWN),
        '-': (Direction.LEFT, Direction.RIGHT),
        'L': (Direction.UP, Direction.RIGHT),
        'J': (Direction.LEFT, Direction.UP),
        '7': (Direction.LEFT, Direction.DOWN),
        'F': (Direction.DOWN, Direction.RIGHT),
    }.get(c)


def parse(f: TextIO) -> Tuple[Tuple[int, int], Grid]:
    grid = {}
    start = None
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            if c == 'S':
                start = (x, y)
            pipe = parse_pipe(c)
            if pipe:
                grid[(x, y)] = pipe

    return start, grid


def format_pipe(pipe: Optional[Pipe]) -> str:
    return {
        (Direction.UP, Direction.DOWN): '│',
        (Direction.LEFT, Direction.RIGHT): '─',
        (Direction.UP, Direction.RIGHT): '└',
        (Direction.LEFT, Direction.UP): '┘',
        (Direction.LEFT, Direction.DOWN): '┐',
        (Direction.DOWN, Direction.RIGHT): '┌',
    }.get(pipe, ' ')


def print_pipes(grid: Grid) -> None:
    xs = [x for x, _ in grid]
    ys = [x for x, _ in grid]
    x0, y0 = min(xs), min(ys)
    x1, y1 = max(xs), max(ys)
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            pipe = grid.get((x, y))
            print(format_pipe(pipe), end='')
        print()


start, grid = parse(sys.stdin)
print(start)
print_pipes(grid)
