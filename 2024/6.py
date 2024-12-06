import sys

def parse(f):
    grid = {}
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            grid[(x, y)] = c
    return grid

DIRECTIONS = [
    (0, -1),  # up
    (1, 0),  # right
    (0, 1),  # down
    (-1, 0),  # left
]

def patrol(grid, position: tuple[int, int]):
    trail = []
    direction = 0
    while position in grid:
        trail.append(position)
        x, y = position
        dx, dy = DIRECTIONS[direction]
        # tun if obstacle
        if grid.get((x + dx, y + dy)) == '#':
            direction = (direction + 1) % len(DIRECTIONS)
        # step foward
        dx, dy = DIRECTIONS[direction]
        position = x + dx, y + dy
    return trail


def find_start(grid) -> tuple[int, int]:
    for position, value in grid.items():
        if value == '^':
            return position
    raise ValueError("Start not found")

def add(p, delta):
    x, y = p
    dx, dy = delta
    return x + dx, y + dy

def is_loop(grid, position) -> bool:
    visited = set()
    direction = 0  # always start upwards
    while position in grid:
        assert grid[position] == '.'
        if (position, direction) in visited:
            return True
        visited.add((position, direction))

        # turn while obstacle infront
        while grid.get(add(position, DIRECTIONS[direction])) == '#':
            direction = (direction + 1) % len(DIRECTIONS)
        # step foward
        position = add(position, DIRECTIONS[direction])
    return False

def find_loops(grid, start):
    free = [p for p, c in grid.items() if c == '.']
    free.remove(start)  # obstacles can't be placed in the start
    loops = []
    for i, position in enumerate(free):
        if i % 256 == 0:
            print(f"{i}/{len(free)}")
        # place obstacle
        assert grid[position] == '.'
        grid[position] = '#'
        if is_loop(grid, start):
            loops.append(position)
        grid[position] = '.'
    return loops

grid = parse(sys.stdin)
start = find_start(grid)
grid[start] = '.'  # clear start
# 1
trail = patrol(grid, start)
print(len(set(trail)))
# 2
loops = find_loops(grid, start)
print(len(loops))
