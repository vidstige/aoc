import sys
from typing import TextIO

Position = tuple[int, int]
Grid = dict[Position, str]

def parse(f: TextIO) -> tuple[Grid, str]:
    lines = (line.rstrip() for line in f)
    # read grid
    grid = {}
    robot = None
    for y, line in enumerate(lines):
        if not line:
            break
        for x, c in enumerate(line):
            if c == '@':
                robot = x, y
            grid[(x, y)] = c

    # join remaining lines
    instructions = ''.join(lines)
    return grid, robot, instructions

DIRECTIONS = {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
}

def push(grid: Grid, p: Position, delta: Position) -> Position:
    x, y = p
    dx, dy = delta
    n = x + dx, y + dy
    # wall -> stop
    if grid[n] == '#':
        return p
    # box -> keep going
    if grid[n] == 'O':
        push(grid, n, delta)
    # now, if there is free space if move robot/box in there
    if grid[n] == '.':
        grid[p], grid[n] = grid[n], grid[p]
        return n
    return p

def execute(grid: Grid, robot: Position, instructions: str):
    for instruction in instructions:
        delta = DIRECTIONS[instruction]
        robot = push(grid, robot, delta)

def print_grid(grid: Grid) -> None:
    xmin, xmax = min(x for x, _ in grid), max(x for x, _ in grid) + 1
    ymin, ymax = min(y for _, y in grid), max(y for _, y in grid) + 1
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            print(grid[(x, y)], end='')
        print()

def gps(grid: Grid) -> int:
    boxes = (p for p, c in grid.items() if c == 'O')
    return sum(x + 100 * y for x, y in boxes)

grid, robot, instructions = parse(sys.stdin)

execute(grid, robot, instructions)
print_grid(grid)
print(gps(grid))
