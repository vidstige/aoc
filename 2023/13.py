from typing import Iterable, Optional, Set, Tuple
import sys

Grid = Set[Tuple[int, int]]

def is_mirror(grid: Grid, line: int) -> bool:
    xmin, xmax = min(x for x, _ in grid), max(x for x, _ in grid) + 1
    midx = (xmax - xmin) // 2
    if line <= midx:
        xs = list(range(xmin, line))
    else:
        xs = list(range(line, xmax))
    ymin, ymax = min(y for _, y in grid), max(y for _, y in grid) + 1
    for y in range(ymin, ymax):
        for x in xs:
            right = (x, y) in grid
            left = (2*line - x - 1, y) in grid
            if left != right:
                #print((x, y), '  ', (2*line - x - 1, y), left, right, 'bad!')
                return False
            #else:
            #    print((x, y), '  ', (2*line - x - 1, y), left, right)
    return True

def find_mirror(grid: Grid) -> Optional[int]:
    xmin, xmax = min(x for x, _ in grid), max(x for x, _ in grid) + 1
    for x in range(xmin + 1, xmax):
        if is_mirror(grid, x):
            return x
    return None
    

def transpose(grid: Grid) -> Grid:
    return {(y, x) for x, y in grid}


def parse() -> Iterable[Grid]:
    current = set()
    y = 0
    for line in sys.stdin:
        if line.rstrip():
            for x, c in enumerate(line):
                if c == '#':
                    current.add((x, y))
            y += 1
        else:
            yield current
            current = set()
            y = 0
    yield current

def print_grid(grid: Grid) -> None:
    xmin, xmax = min(x for x, _ in grid), max(x for x, _ in grid) + 1
    ymin, ymax = min(y for _, y in grid), max(y for _, y in grid) + 1
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            print('#' if (x, y) in grid else '.', end='')
        print()


#grids = list(parse())
#grid = transpose(grids[20])
#print_grid(grid)
#print(find_mirror(grid))
#exit()

sum = 0
for i, grid in enumerate(parse()):
    xr = find_mirror(grid)
    if xr:
        sum += xr
    else:
        yr = find_mirror(transpose(grid))
        sum += yr * 100

print(sum)


