
def bounding_box(grid):
    xmin = min(x for x, _ in grid)
    xmax = max(x for x, _ in grid)
    ymin = min(y for _, y in grid)
    ymax = max(y for _, y in grid)
    return xmin, xmax + 1, ymin, ymax + 1

def draw(grid, bounds=None, X=None):
    if not grid:
        return
    xmin, xmax, ymin, ymax = bounds or bounding_box(grid)
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            if (x, y) == X:
                character = 'X'
            else:
                character = grid.get((x, y), ' ')
            print(character, end='')
        print()
