from itertools import product
import sys

D = 4

# relative neighbors
NEIGHBORS = set(product((-1, 0, 1), repeat=D))
ORIGO = (0, ) * D
NEIGHBORS.remove(ORIGO)

def parse(f):
    grid = set()
    for y, line in enumerate(f):
        for x, char in enumerate(line):
            if char == '#':
                grid.add((x, y, 0, 0))
    return grid

def add(a, b):
    return tuple(ai + bi for ai, bi in zip(a, b))

def neighbors(p):
    return [add(p, rn) for rn in NEIGHBORS]

def active(grid, ps):
    return len([1 for p in ps if p in grid])

def step(grid):
    # precompute neighbors
    ns = {p: neighbors(p) for p in grid}
    work = grid.union(*ns.values())
    # compute neighbors of neighbors
    ns.update({n: neighbors(n) for n in work})
    return {p for p in work if (p in grid and active(grid, ns[p]) in (2, 3)) or (p not in grid and active(grid, ns[p]) == 3)}

grid = parse(sys.stdin)
for i in range(6):
    grid = step(grid)
print(len(grid))
