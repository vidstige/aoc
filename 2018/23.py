import re

def rev(t: tuple) -> tuple:
    return tuple(reversed(t))

def load(filename):
    with open(filename) as f:
        for line in f:
            match = re.match(r'pos=<(-?[\d]+),(-?[\d]+),(-?[\d]+)>, r=([\d]+)', line)
            if match:
                x, y, z, r = map(int, match.groups())
                yield r, x, y, z
            else:
                raise Exception('line' + line)

def manhattan(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return abs(bx - ax) + abs(by - ay) + abs(bz - az)

def radius(bot):
    return bot[0]

from collections import defaultdict

def placement_separated(bots, dimension):
    within = defaultdict(int)
    for bot in bots:
        for delta in range(-radius(bot), radius(bot)):
            c = bot[dimension] + delta
            within[c] += 1
    high = max(within.values())
    return [k for k, v in within.items() if v == high]

def cube(xs, ys, zs):
    for z in zs:
        for y in ys:
            for x in xs:
                yield x, y, z

def placement(bots):
    origin = (0, 0, 0)

    candidates = cube(placement_separated(bots, 1), placement_separated(bots, 2), placement_separated(bots, 3))
    #for c in candidates:
    #    print(c)
    m = min((manhattan(origin, candidate), candidate) for candidate in candidates)
    print(m)

bots = list(load('input/23ex2'))
print(bots)
print(placement(bots))
#strong = max(bots)
#print(len([b for b in bots if manhattan(b, strong) <= radius(strong)]))
