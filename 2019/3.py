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

def manhattan(p):
    x, y = p
    return abs(x) + abs(y)


def walk(wire):
    grid = {}
    x, y = 0, 0
    steps = 0
    for direction, distance in wire:
        dx, dy = DIRECTIONS[direction]
        for _ in range(distance):
            if (x, y) not in grid:
                grid[(x, y)] = steps
            steps += 1
            x, y = x + dx, y + dy
    return grid

def intersections(wires):
    a, b = wires
    ga = walk(a)
    gb = walk(b)
    intersections = set(ga.keys()).intersection(set(gb.keys()))
    intersections.remove((0, 0))
    return zip([ga[i] for i in intersections], [gb[i] for i in intersections])

def closest_intersection(data):
    #origo = (0, 0)
    return min(sum(p) for p in intersections(parse(data)))
    #return intersections(parse(data))

print(closest_intersection(ex1))
print(closest_intersection(ex2))
print(closest_intersection(load()))