DIRECTIONS = {
    'nw': (-1, -1),
    'n': (0, -2),
    'ne': (1, -1),
    
    'se': (1, 1),
    's': (0, 2),
    'sw': (-1, 1)
}


def step(direction, p):
    dx, dy = DIRECTIONS[direction]
    x, y = p
    return (x + dx, y + dy)

def distance(a, b):
    """Greedy search"""
    def L1(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x2 - x1) + abs(y2 - y1)

    n = 0
    p = a

    # 1. go sideways until on correct x.
    SIDEWAYS = ['nw', 'ne', 'sw', 'se']
    while p[0] != b[0]:
        distances = {d: L1(step(d, p), b) for d in SIDEWAYS}        
        delta = min(distances, key=distances.get)
        p = step(delta, p)
        n += 1

    # 2. go up/down until correct position
    while p != b:
        distances = {d: L1(step(d, p), b) for d in ['s', 'n']}
        delta = min(distances, key=distances.get)
        p = step(delta, p)
        n += 1

    return n


def walk(data):
    p = (0, 0)
    start = p
    distances = []
    for dir in data.split(','):
        p = step(dir, p)
        distances.append(distance(start, p))
    
    end = p
    return distances


ex = {
    'ne,ne,ne': 3,
    'ne,ne,sw,sw': 0,
    'ne,ne,s,s': 2,
    'se,sw,se,sw,sw': 3
}

for data, expected in ex.items():
    actual = walk(data)[-1]
    print("{mark} {actual} == {expected}".format(
        mark='✔' if actual == expected else 'x',
        actual=actual, expected=expected
    ))
    

with open('input/11') as f:
    data = f.read()
    print(max(walk(data)))