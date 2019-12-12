from itertools import combinations
from math import copysign

data="""<x=6, y=10, z=10>
<x=-9, y=3, z=17>
<x=9, y=-4, z=14>
<x=4, y=14, z=4>"""

ex1 = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

ex2="""<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""

def fmt_vector(vector):
    return '<x={}, y={}, z={}>'.format(*vector)

class Moon:
    def __init__(self, p, v=None):
        self.position = p
        self.velocity = v or (0, 0, 0)
    def __repr__(self):
        return "pos={}, vel={}".format(fmt_vector(self.position), fmt_vector(self.velocity))

def parse(data):
    def parse_moon(line):
        parts = line.lstrip('<').rstrip('>').split(', ')
        coords = [tuple(c.split('=')) for c in parts]
        return Moon(tuple(int(value) for key, value in coords))

    return [parse_moon(moon) for moon in data.splitlines()]

def axis_force(ca, cb):
    if cb > ca:
        return 1
    if ca > cb:
        return -1
    return 0

def add(a, b):
    return tuple(ca + cb for ca, cb in zip(a, b))

def gravity(pa, pb):
    return tuple(axis_force(ca, cb) for ca, cb in zip(pa, pb))
        

def step(moons):
    for ma, mb in combinations(moons, 2):
        ma.velocity = add(ma.velocity, gravity(ma.position, mb.position))
        mb.velocity = add(mb.velocity, gravity(mb.position, ma.position))
    for moon in moons:
        moon.position = add(moon.position, moon.velocity)


def energy(moon):
    kinetic = sum(abs(c) for c in moon.velocity)
    potential = sum(abs(c) for c in moon.position)
    return kinetic * potential

def simulate(data, until):
    moons = parse(data)
    for t in range(until):
        step(moons)

    for moon in moons:
        print(moon)
    print(sum(energy(moon) for moon in moons))


simulate(ex1, until=10)
simulate(ex2, until=100)
simulate(data, until=1000)
