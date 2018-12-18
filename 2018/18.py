def load(filename):
    grid = {}
    with open(filename) as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line):
                if c in '#|':
                    grid[(x, y)] = c
    return grid

def bounding(grid):
    xmin = min(x for x, _ in grid)
    xmax = max(x for x, _ in grid)
    ymin = min(y for _, y in grid)
    ymax = max(y for _, y in grid)
    return xmin, xmax + 1, ymin, ymax + 1


def row_major(bounds):
    xmin, xmax, ymin, ymax = bounds
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            yield x, y

def adjacent(p):
    x, y = p
    yield x - 1, y - 1
    yield x, y - 1
    yield x + 1, y - 1
    yield x - 1, y
    yield x + 1, y
    yield x - 1, y + 1
    yield x, y + 1
    yield x + 1, y + 1

def minute(grid, bounds):
    n = {}
    for p in row_major(bounds):
        trees = len([a for a in adjacent(p) if grid.get(a) == '|'])
        lumberyards = len([a for a in adjacent(p) if grid.get(a) == '#'])
        # stay the same by default
        if p in grid:
            n[p] = grid[p]
        if p not in grid and trees >= 3:
            n[p] = '|'
        if grid.get(p) == '|' and lumberyards >= 3:
            n[p] = '#'
        if grid.get(p) == '#':
            if trees >= 1 and lumberyards >= 1:
                pass
            else:
                del n[p]

    return n

def draw(grid, bounds):
    xmin, xmax, ymin, ymax = bounds
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            print(grid.get((x, y), ' '), end='')
        print()

def main():
    grid = load('input/18')
    bounds = bounding(grid)
    for _ in range(10):
        draw(grid, bounds)
        grid = minute(grid, bounds)
    trees = sum(1 for v in grid.values() if v == '|')
    lumberyards = sum(1 for v in grid.values() if v == '#')
    print(trees, lumberyards, trees * lumberyards)

main()
