from itertools import combinations
from math import gcd

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

print(visible(parse(ex1)))
print(visible(parse(ex2)))
print(visible(parse(ex3)))
print(visible(parse(ex4)))
print(visible(parse(ex5)))
print(visible(parse(load())))
