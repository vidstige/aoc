from collections import defaultdict
import sys

Position = tuple[int, int]
Grid = dict[Position, str]

def parse() -> Grid:
    grid = {}
    for y, line in enumerate(sys.stdin):
        for x, c in enumerate(line.rstrip()):
            grid[(x, y)] = c
    return grid


NEIGHBOURS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]
FENCES = [
    ((0, 0), (1, 0)),  # top
    ((1, 0), (1, 1)),  # right
    ((1, 1), (0, 1)),  # bottom
    ((0, 1), (0, 0)),  # left 
]

def find_regions(grid: Grid):
    while grid:
        position, crop = grid.popitem()
        positions = set()
        nodes = [position]
        while nodes:
            x, y = nodes.pop()
            positions.add((x, y))
            for dx, dy in NEIGHBOURS:
                np = x + dx, y + dy
                if grid.get(np) == crop:
                    del grid[np]
                    nodes.append(np)
        yield positions


def area(region: set[Position]) -> int:
    return len(region)

def perimeter(region: set[Position]) -> int:
    p = 0
    for x, y in region:
        p += 4 - sum(1 for dx, dy in NEIGHBOURS if (x + dx, y + dy) in region)
    return p

def price(region: set[Position]) -> int:
    return area(region) * perimeter(region)

def sides(region: set[Position]) -> int:
    # first compute all the pieces of the fence
    pieces = set()  # pairs of position, delta
    for x, y in region:
        for (dx, dy), ((ax, ay), (bx, by)) in zip(NEIGHBOURS, FENCES):
            if (x + dx, y + dy) not in region:
                # fence piece needed
                pieces.add(((x + ax, y + ay), (bx - ax, by - ay)))
    
    # fuse pieces into sides
    sides = []
    while pieces:
        # start with any piece still remaining
        (px, py), (dx, dy) = pieces.pop()
        side = [((x, y), (dx, dy))]

        # go right
        x, y = px, py
        while ((x + dx, y + dy), (dx, dy)) in pieces:
            pieces.remove(((x + dx, y + dy), (dx, dy)))
            side.append(((x + dx, y + dy), (dx, dy)))
            x, y = x + dx, y + dy

        # go left
        x, y = px, py
        while ((x - dx, y - dy), (dx, dy)) in pieces:
            pieces.remove(((x - dx, y - dy), (dx, dy)))
            side.append(((x - dx, y - dy), (dx, dy)))
            x, y = x - dx, y - dy
        sides.append(side)

    return len(sides)

grid = parse()
regions = list(find_regions(grid))
#total = sum(price(region) for region in regions)
#print(total)

total2 = sum(area(region) * sides(region) for region in regions)
print(total2)
