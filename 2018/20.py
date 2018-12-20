def draw(grid, bounds):
    xmin, xmax, ymin, ymax = bounds
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            if (x, y) == (0, 0):
                print('X', end='')
            else:
                print(grid.get((x, y), '#'), end='')
        print()

def bounds(grid):
    xmin = min(x for x, _ in grid)
    xmax = max(x for x, _ in grid)
    ymin = min(y for _, y in grid)
    ymax = max(y for _, y in grid)
    return xmin, xmax + 1, ymin, ymax + 1

directions = {
    'E': (2, 0, '|'),
    'W': (-2, 0, '|'),
    'N': (0, -2, '-'),
    'S': (0, 2, '-')
}

def search(regexp):
    grid = {}
    stack = []
    p = 0, 0
    for c in regexp:
        grid[p] = '.'
        if c in directions:
            dx, dy, door = directions[c]
            x, y = p
            grid[(x + dx // 2, y + dy // 2)] = door
            p = x + dx, y + dy
        if c == '(':
            stack.append(p)
        if c == '|':
            p = stack[-1]
        if c == ')':
            p = stack.pop()

    return grid

print(directions.values())
def shortest(grid):
    stack = [((0,0), 0)]
    visited = {}
    high = 0
    while stack:
        (x, y), distance = stack.pop()
        if distance > high:
            high = distance
        visited[(x, y)] = 3
        for dx, dy, _ in directions.values():
            nw = x + dx // 2, y + dy // 2
            if grid.get(nw, ' ') in '|-':
                n = x + dx, y + dy
                if n not in visited:
                    stack.append((n, distance + 1))
    return high



def main():
    print(shortest(search('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$')))
    print(shortest(search('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$')))

    with open('input/20') as f:
        print(shortest(search(f.read())))
main()
