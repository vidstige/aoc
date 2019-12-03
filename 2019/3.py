def parse_instruction(tmp):
    direction = tmp[0]
    distance = int(tmp[1:])
    return direction, distance

def parse(data):
    return tuple([parse_instruction(tmp) for tmp in wire.split(',')] for wire in data.split('\n'))

def load():
    with open('input/3') as f:
        return f.read()

ex1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83'
ex2 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7'

DIRECTIONS = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, -1),
    'D': (0, 1)
}

def is_horizontal(direction):
    return direction in ('L', 'R')

def is_vertical(direction):
    return direction in ('U', 'D')

def line_segments(wire):
    """split wires into line segments"""
    vertical = []
    horizontal = []
    x, y = 0, 0
    for segment in wire:
        ox, oy = x, y
        direction, distance = segment
        dx, dy = DIRECTIONS[direction]
        x += dx * distance
        y += dy * distance
        line = (min(ox, x), min(oy, y), max(ox, x), max(oy, y))
        if is_horizontal(direction):
            horizontal.append(line)
        if is_vertical(direction):
            vertical.append(line)
    return horizontal, vertical


def manhattan(p):
    x, y = p
    return abs(x) + abs(y)

def intersect(h, v):
    """intersects a horizontal and vertical line segment"""
    hx0, hy0, hx1, hy1 = h
    vx0, vy0, vx1, vy1 = v
    if hy0 >= vy0 and hy0 <= vy1:
        if vx0 >= hx0 and vx0 <= hx1:
            return vx0, hy0

    return False

def intersections_vh(a, b):
    has, vas = a
    hbs, vbs = b
    for ha in has:
        for vb in vbs:
            interection = intersect(ha, vb)
            if interection:
                yield interection

    for va in vas:
        for hb in hbs:
            interection = intersect(hb, va)
            if interection:
                yield interection

        
def intersections(wires):
    a, b = wires
    lsa = line_segments(a)
    lsb = line_segments(b)
    
    return list(intersections_vh(lsa, lsb))

def closest_intersection(data):
    origo = (0, 0)
    return min(manhattan(p) for p in intersections(parse(data)) if p != origo)

print(closest_intersection(ex1))
print(closest_intersection(ex2))
print(closest_intersection(load()))