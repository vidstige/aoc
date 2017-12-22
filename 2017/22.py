def grid2lines(grid, p=None):
    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)
    min_x = min(x for x, y in grid)
    min_y = min(y for x, y in grid)
    lines = []
    for y in range(min_y, max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            if p == (x, y):
                line.append('O')
            else:
                line.append('#' if (x, y) in grid else '.')
        lines.append(' '.join(line))
    return lines

def lines2grid(lines):
    grid = {}
    for y, line in enumerate(lines):
        for x, v in enumerate(line):
            if v == '#':
                grid[(x, y)] = 'infected'
    return grid

def turn_right(dx, dy):
    return (-dy, dx)
def turn_left(dx, dy):
    return (dy, -dx)

def main(lines):
    infected = lines2grid(lines)
    mid = len(lines) // 2
    x, y = mid, mid
    dx, dy = 0, -1

    count = 0
    for _ in range(10000):
        if (x, y) in infected:
            dx, dy = turn_right(dx, dy)
        else:
            dx, dy = turn_left(dx, dy)
        
        if (x, y) in infected:
            del infected[(x, y)]
        else:
            infected[(x, y)] = True
            count += 1
        
        #print("\n")
        #print('\n'.join(grid2lines(infected, (x,y))))

        x, y = x + dx, y + dy
    print(count)

ex = """..#
#..
...""".splitlines()
#main(ex)

with open('input/22') as f:
    lines = f.readlines()
    main(lines)

