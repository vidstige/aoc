def spiral(n, x0=0, y0=0):
    x = x0
    y = y0

    dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    d = 0  # direction. index to dirs array
    i = 0  # current number
    s = 0  # segment length so far
    l = 1  # wanted segment length
    while i < n:
        yield (x, y)

        dx, dy = dirs[d]
        x += dx
        y += dy
        s += 1
        
        if s >= l:
            s = 0
            if d == 0:  # when finishing "right"
                pass
            if d == 1:  # when finishing "down"
                l += 1
            if d == 2:  # when finishing "left"
                pass
            if d == 3:  # when finishing "up"
                l += 1
            d = (d + 1) % len(dirs)

        i += 1

def adjacent(p):
    """returns the coordinates of the 8 adjacent 
    coordinates"""
    x, y = p
    return [
        (x-1, y-1),
        (x+0, y-1),
        (x+1, y-1),
        
        (x-1, y+0),
        (x+1, y+0),

        (x-1, y+1),
        (x+0, y+1),
        (x+1, y+1)
        ]

def sum_adjacent():
    # initialize center to 1
    values = {(0, 0): 1}
    for p in spiral(100000000):
        s = sum(values.get(x, 0) for x in adjacent(p))
        if p not in values:
            values[p] = s
        yield s

print(next(s for s in sum_adjacent() if s > 277678))
