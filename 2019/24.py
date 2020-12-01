ex1="""....#
#..#.
#..##
..#..
#...."""
ex2="""....#
#..#.
#.?##
..#..
#...."""

data="""##...
#.###
.#.#.
#....
..###"""

def parse(data):
    bugs = set()
    for y, line in enumerate(data.splitlines()):
        for x, character in enumerate(line):
            if character == '#':
                bugs.add((x - 2, y - 2, 0))
    return bugs

def neighbours(x, y):
    yield x, y - 1
    yield x - 1, y
    yield x + 1, y
    yield x, y + 1

def neighbours2(bug):
    x, y, z = bug
    # outer edges
    
    # top neighbours
    if y == -2:
        yield 0, -1, z - 1    
    elif y == 1 and x == 0:
        for xx in range(5):
            yield xx - 2, 2, z + 1
    else:
        yield x, y - 1, z
    
    # bottom neighbours
    if y == 2:
        yield 0, 1, z - 1
    elif y == -1 and x == 0:
        for xx in range(5):
            yield xx - 2, -2, z + 1
    else:
        yield x, y + 1, z
    
    # left neighbours
    if x == -2:
        yield -1, 0, z - 1
    elif x == 1 and y == 0:
        for yy in range(5):
            yield 2, yy - 2, z + 1
    else:
        yield x - 1, y, z

    # right neighbours
    if x == 2:
        yield 1, 0, z - 1
    elif x == -1 and y == 0:
        for yy in range(5):
            yield -2, yy - 2, z + 1
    else:
        yield x + 1, y, z

def bounding(grid):
    xmin = min(x for x, _, _ in grid)
    xmax = max(x for x, _, _ in grid)
    ymin = min(y for _, y, _ in grid)
    ymax = max(y for _, y, _ in grid)
    zmin = max(z for _, _, z in grid)
    zmax = max(z for _, _, z in grid)
    return xmin, xmax + 1, ymin, ymax + 1, zmin, zmax + 1

def draw(grid, bounds=None):
    xmin, xmax, ymin, ymax = bounds or bounding(grid)
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            p = x, y
            print('#' if p in grid else '.', end='')
        print()

def evolve(bugs):
    result = set()
    # all neoihboys
    everything = set(bugs)
    for bug in bugs:
        for n in neighbours2(bug):
            everything.add(n)

    for p in everything:
        i = len([n for n in neighbours2(p) if n in bugs])
        if p in bugs:
            if i == 1:
                result.add(p)
        else:
            if i in (1, 2):
                result.add(p)
    return result

def biodiversity(bugs, bounds):
    xmin, xmax, ymin, ymax = bounds or bounding(bugs)
    pts = 1
    result = 0
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            if (x, y) in bugs:
                result += pts
            pts *= 2
    return result

def solve(data, t):
    bugs = parse(data)
    #print(bounding(bugs))
    for _ in range(t):
        bugs = evolve(bugs)
    
    print(len(bugs))
    #print(bounding(bugs))

solve(ex2, t=10)
solve(data, t=200)