from collections import defaultdict
from itertools import combinations
from math import gcd, atan2

ex1 = """.#..#
.....
#####
....#
...##"""

ex2="""......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

ex3="""#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""

ex4=""".#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""

ex5=""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

def parse(data):
    grid = set()
    for y, line in enumerate(data.splitlines()):
        for x, character in enumerate(line.rstrip()):
            if character == '#':
                grid.add((x, y))
    return grid

def load():
    with open('input/10') as f:
        return f.read()

def blocks(a, b, p):
    """Returns true if the point p blocks the vision between a and b"""
    if a == p or b == p:
        return False
    ax, ay = a
    bx, by = b
    px, py = p

    dx0, dy0 = px - ax, py - ay
    dx1, dy1 = bx - px, by - py

    gcd0 = gcd(dx0, dy0)
    dx0, dy0 = dx0 // gcd0, dy0 // gcd0
    gcd1 = gcd(dx1, dy1)
    dx1, dy1 = dx1 // gcd1, dy1 // gcd1
    return dx0 == dx1 and dy0 == dy1


def visible(astroids):
    visibility = set()
    for a, b in combinations(astroids, 2):
        if a == b:
            continue
        if not any(blocks(a, b, p) for p in astroids):
            visibility.add(frozenset([a, b]))

    return max((len([v for v in visibility if a in v]), a) for a in astroids)

def center_on(astroids, center):
    cx, cy = center
    deltas = defaultdict(list)
    for x, y in astroids:
        dx, dy = x - cx, y - cy
        t = gcd(dx, dy)
        if t > 0:
            d = (dx // t, dy // t)
            deltas[d].append(t)
    for ts in deltas.values():
        ts.sort(reverse=True)
    return deltas

def rotation(delta):
    return atan2(*delta)

def laser(astroids, center):
    #astroids = parse(ex5)
    cx, cy = center
    deltas = center_on(astroids, (cx, cy))
    i = 0
    while any(ts for ts in deltas.values()):
        for d in sorted(deltas, key=rotation, reverse=True):
            # laser
            if deltas[d]:
                t = deltas[d].pop()
                dx, dy = d
                print(i+1, cx+dx*t, cy+dy*t)
                i += 1

#print(visible(parse(ex1)))
#print(visible(parse(ex2)))
#print(visible(parse(ex3)))
#print(visible(parse(ex4)))
#print(visible(parse(ex5)))
#print(visible(parse(load())))

laser(parse(load()), (20, 19))

