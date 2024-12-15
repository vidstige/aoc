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

def can_push(grid: Grid, p: Position, delta: Position) -> bool:
    x, y = p
    dx, dy = delta
    n = x + dx, y + dy
    # wall -> stop
    if grid[n] == '#':
        return False
    if grid[n] == 'O':
        return can_push(grid, n, delta)
    # left side of a box
    if grid[n] == '[':
        if dx == 0:  # if up/down push
            return can_push(grid, n, delta) and can_push(grid, (x + dx + 1, y + dy), delta)
        else: # left/right push
            return can_push(grid, n, delta)
    # right side of box
    if grid[n] == ']':
        if dx == 0:
            return can_push(grid, n, delta) and can_push(grid, (x + dx - 1, y + dy), delta)
        else:
            return can_push(grid, n, delta)
    assert grid[n] in '.@', grid[n]
    return True


def push(grid: Grid, p: Position, delta: Position) -> Position:
    x, y = p
    dx, dy = delta
    n = x + dx, y + dy
    assert grid[n] != '#'
    if grid[n] == 'O':
        push(grid, n, delta)
    # left side of a box
    if grid[n] == '[':
        push(grid, n, delta)
        if dx == 0: # up/down push. Also push other side
            push(grid, (x + dx + 1, y + dy), delta)
    # right side of box
    if grid[n] == ']':
        push(grid, n, delta)
        if dx == 0: # up/down push. Also push other side
            push(grid, (x + dx - 1, y + dy), delta)
    # either way, swap items here
    grid[p], grid[n] = grid[n], grid[p]
    return n

def execute(grid: Grid, robot: Position, instructions: str):
    for instruction in instructions:
        delta = DIRECTIONS[instruction]
        if can_push(grid, robot, delta):
            robot = push(grid, robot, delta)

def print_grid(grid: Grid) -> None:
    xmin, xmax = min(x for x, _ in grid), max(x for x, _ in grid) + 1
    ymin, ymax = min(y for _, y in grid), max(y for _, y in grid) + 1
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            print(grid[(x, y)], end='')
        print()

def gps(grid: Grid) -> int:
    boxes = (p for p, c in grid.items() if c in 'O[')
    return sum(x + 100 * y for x, y in boxes)

def widen(grid: Grid, robot: Position) -> tuple[Grid, Position]:
    WIDE = {
        '.': '..',
        'O': '[]',
        '@': '@.',
        '#': '##',
    }
    tmp = {}
    for (x, y), c in grid.items():
        for dx, cc in enumerate(WIDE[c]):
            tmp[(2 * x + dx, y)] = cc
    x, y = robot
    return tmp, (2*x, y)

grid, robot, instructions = parse(sys.stdin)

# part 1
execute(grid, robot, instructions)
print_grid(grid)
print(gps(grid))

# part 2
wide, robot = widen(grid, robot)
execute(wide, robot, instructions)
print_grid(wide)
print(gps(wide))
