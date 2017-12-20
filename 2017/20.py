import re
from itertools import combinations

PATTERN = "p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>"

def magnitude(v):
    x, y, z = v
    return abs(x) + abs(y) + abs(z)

def add(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return ax+bx, ay+by, az+bz

def eq(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return ax == bx and ay == by and az == bz


class Particle(object):
    def __init__(self, p, v, a):
        self.p = p
        self.v = v
        self.a = a

    def update(self):
        self.v = add(self.v, self.a)
        self.p = add(self.p, self.v)


def collides(a, b):
    return eq(a.p, b.p)

def parse_particles(lines):
    for line in lines:
        match = re.match(PATTERN, line)
        px, py, pz, vx, vy, vz, ax, ay, az = match.groups()
        p = (int(px), int(py), int(pz))
        v = (int(vx), int(vy), int(vz))
        a = (int(ax), int(ay), int(az))
        yield Particle(p, v, a)


def main():
    with open('input/20') as f:
        lines = f.readlines()
    
    particles = list(parse_particles(lines))
    m, i = min((magnitude(p.a), i) for i, p in enumerate(particles))
    print(i)    

    for _ in range(100):
        for p in particles:
            p.update()

        colliding = set()
        for a, b in combinations(particles, 2):
            if collides(a, b):
                colliding.add(a)
                colliding.add(b)

        for p in colliding:
            particles.remove(p)

        print(len(particles))


main()
