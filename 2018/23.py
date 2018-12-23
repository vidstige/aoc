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
    _, ax, ay, az = a
    _, bx, by, bz = b
    return abs(bx - ax) + abs(by - ay) + abs(bz - az)

def radius(bot):
    return bot[0]

bots = list(load('input/23'))
strong = max(bots)

print(len([b for b in bots if manhattan(b, strong) <= radius(strong)]))
