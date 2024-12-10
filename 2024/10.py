import sys

Position = tuple[int, int]
Grid = dict[Position, int]

def parse(f) -> Grid:
    grid = {}
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            grid[(x, y)] = int(c)
    return grid

def find_trailheads(grid: Grid) -> list[Position]:
    return [position for position, height in grid.items() if height == 0]

NEIGHBOURS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]

def search(grid: Grid, start: Position):
    nodes = [(start, tuple())]
    while nodes:
        node, path = nodes.pop()
        if grid[node] == 9:
            yield path
        x, y = node
        neighbours = [(x + dx, y + dy) for dx, dy in NEIGHBOURS if grid[(x, y)] + 1 == grid.get((x + dx, y + dy))]
        for neighbour in neighbours:
            nodes.append((neighbour, path + (neighbour,)))
    return total


grid = parse(sys.stdin)
total = 0
for trailhead in find_trailheads(grid):
    paths = set(search(grid, trailhead))
    total += len(paths)

print(total)