def load(filename):
    a = {
        '<': '-',
        '>': '-',
        '^': '|',
        'v': '|'
    }

    with open(filename) as f:
        tracks = {}
        carts = {}
        for y, row in enumerate(f.readlines()):
            for x, col in enumerate(row.rstrip()):
                p = x, y
                #if col != ' ':
                tracks[p] = a.get(col, col)
                if col in a:
                    carts[p] = (col, 0)
        return tracks, carts


def rev(t: tuple) -> tuple:
    return tuple(reversed(t))


def display(tracks, carts):
    row_y = None
    row = []
    for x, y in sorted(tracks, key=rev):
        if y != row_y:
            if row:
                print(''.join(row))
            row = []
            row_y = y
        p = x, y
        row.append(carts.get(p, tracks[p])[0])
    print(''.join(row))

def tick(tracks, carts):
    d = {
        '>': (1, 0),
        '<': (-1, 0),
        '^': (0, -1),
        'v': (0, 1)
    }
    turns = {
        '>\\': 'v',
        '>/': '^',
        '<\\': '^',
        '</': 'v',
        'v\\': '>',
        'v/': '<',
        '^\\': '<',
        '^/': '>'
    }
    intersections = {
        '>0': '^',
        '>1': '>',
        '>2': 'v',

        '<0': 'v',
        '<1': '<',
        '<2': '^',

        'v0': '>',
        'v1': 'v',
        'v2': '<',

        '^0': '<',
        '^1': '^',
        '^2': '>'
    }
    c = {}
    for p in sorted(carts, key=rev):
        x, y = p
        direction, t = carts[p]
        dx, dy = d[direction]
        pp = x + dx, y + dy
        if pp in c:
            print(pp)
            return None
        
        new = tracks[pp]
        if new == '+':
            c[pp] = intersections['{}{}'.format(direction, t % 3)], t + 1
        else:
            c[pp] = turns.get('{}{}'.format(direction, new), direction), t
        
    return c


def verify(tracks, carts):
    for p in carts:
        if tracks[p] not in '|-\\/+':
            print('Card standing on {} at {}.'.format(tracks[p], p))


tracks, carts = load('input/13')
display(tracks, carts)
while carts:
    verify(tracks, carts)
    #display(tracks, carts)
    #print()
    carts = tick(tracks, carts)

#display(tracks, carts)
