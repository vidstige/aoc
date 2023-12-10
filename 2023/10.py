from enum import IntEnum
import sys
from typing import Dict, Iterable, Optional, TextIO, Tuple

Position = Tuple[int, int]

class Direction(IntEnum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    def delta(self) -> Position:
        return {
            Direction.LEFT: (-1, 0),
            Direction.UP: (0, -1),
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, 1),
        }[self]
    
    def reverse(self) -> 'Direction':
        return {
            Direction.LEFT: Direction.RIGHT,
            Direction.UP: Direction.DOWN,
            Direction.RIGHT: Direction.LEFT,
            Direction.DOWN: Direction.UP,
        }[self]


Pipe = Tuple[Direction, Direction]

Grid = Dict[Position, Pipe]


def parse_pipe(c: str) -> Optional[Pipe]:
    return {
        '|': (Direction.UP, Direction.DOWN),
        '-': (Direction.LEFT, Direction.RIGHT),
        'L': (Direction.UP, Direction.RIGHT),
        'J': (Direction.LEFT, Direction.UP),
        '7': (Direction.LEFT, Direction.DOWN),
        'F': (Direction.RIGHT, Direction.DOWN),
    }.get(c)


def add(p: Position, delta: Position) -> Position:
    x, y = p
    dx, dy = delta
    return x + dx, y + dy


def parse(f: TextIO) -> Tuple[Position, Grid]:
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
        (Direction.RIGHT, Direction.DOWN): '┌',
    }.get(pipe, '·')


def print_pipes(grid: Grid, mask: Dict[Position, str] = {}) -> None:
    xs = [x for x, _ in grid]
    ys = [y for _, y in grid]
    x0, y0 = min(xs), min(ys)
    x1, y1 = max(xs), max(ys)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            p = x, y
            overwrite = mask.get(p)
            if overwrite:
                c = overwrite
            else:
                pipe = grid.get(p)
                c = format_pipe(pipe)
            print(c, end='')
        print()


def fill_start(grid: Grid, start: Position) -> None:
    outgoing = []
    for direction in Direction:
        delta = direction.delta()
        for dir in grid.get(add(start, delta), ()):
            if dir == direction.reverse():
                outgoing.append(direction)
    assert len(outgoing) == 2, "Can't guess start pipe"
    grid[start] = tuple(sorted(outgoing))


def follow(grid: Grid, start: Position) -> Iterable[Position]:
    p = start
    skip = None  # start in any direction
    
    # keep going until we reach start again
    while p != start or skip is None:
        directions = grid[p]
        direction = next(d for d in directions if d != skip)
        #print('going', direction)
        skip = direction.reverse()
        p = add(p, direction.delta())
        yield p


def is_horizontal(pipe: Pipe) -> bool:
    return pipe == (Direction.LEFT, Direction.RIGHT)


def interior(grid: Grid, start: Position) -> Iterable[Position]:
    """Computes area enclosed by pipe starting at 'start'"""
    outline = set(follow(grid, start))
    # remove horizontal pipes
    horizontal = {p for p in outline if is_horizontal(grid[p])}
    cuts = outline - horizontal
    # bounding box
    xs = [x for x, _ in grid]
    ys = [x for x, _ in grid]
    x0, y0 = min(xs), min(ys)
    x1, y1 = max(xs), max(ys)
    # scan each line
    for y in range(y0, y1 + 1):
        # keep track of starts of both UP and DOWN pipes
        inside: Dict[Direction, bool] = {Direction.UP: False, Direction.DOWN: False}
        for x in range(x0, x1 + 1):
            p  = x, y
            if p in outline:
                for direction in inside:
                    if direction in grid[p]:
                        inside[direction] = not inside[direction]
            if all(inside.values()) and p not in outline:
                yield p


start, grid = parse(sys.stdin)
fill_start(grid, start)

#path = list(follow(grid, start))
#print(len(path) // 2)

pipe_interor = list(interior(grid, start))
print_pipes(grid, mask={p: 'I' for p in pipe_interor})
print(len(pipe_interor))
