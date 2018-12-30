from tqdm import tqdm
from functools import lru_cache

def hundreds(x):
    return int(str(x // 100)[-1])


def cell(serial, p):
    x, y = p
    rack_id = x + 10
    level = (rack_id * y + serial) * rack_id
    return hundreds(level) - 5


def grid(w, h, sx=0, sy=0):
    for y in range(w):
        for x in range(h):
            yield sx + x, sy + y

@lru_cache()
def compute_power_grid(serial, size=300):
    power_grid = {}
    for x, y in grid(size, size):
        p = x+1, y+1
        power_grid[p] = cell(serial, p)
    return power_grid

def power_levels(levels, power_grid, kernel=3, size=300):
    for x, y in grid(size - kernel, size - kernel):
        levels[(x+1, y+1, kernel)] = sum(power_grid[(x+1 + a, y+1 + b)] for a, b in grid(kernel, kernel))
    return levels

def highest(levels):
    return max((l, c) for c, l in levels.items())

#print(cell(71, (101,153)))
#print(18, highest(power_levels(18)))
#print(42, highest(power_levels(42)))

# 1
#print(1955, highest(power_levels(1955)))

from collections import defaultdict

@lru_cache()
def compute_sat(serial, size=300):
    sat = defaultdict(int)
    for x, y in grid(size + 1, size + 1):
        sat[(x, y)] = \
            cell(serial, (x, y)) + \
            sat[(x - 1, y)] + \
            sat[(x, y - 1)] - \
            sat[(x - 1, y - 1)]
    return dict(sat)

def power(serial, x, y, s):
    sat = compute_sat(serial)
    return sat[(x + s - 1, y + s - 1)] + sat[(x - 1, y - 1)] - sat[(x + s - 1, y - 1)] - sat[(x - 1, y + s - 1)]

def simple_power(serial, x, y, s):
    return sum(cell(serial, p) for p in grid(s, s, sx=x, sy=y))

def search(serial):
    for s in tqdm(reversed(range(1, 300)), total=300):
        for x, y in grid(300 - s, 300 - s):
            yield power(serial, x, y, s), x, y, s

def draw(serial, size=300):
    for y in range(size):
        for x in range(size):
            print('{: >4}'.format(cell(serial, (x, y))), end='')
        print()

def draw_sat(serial, size=300):
    sat = compute_sat(serial)
    for y in range(size):
        for x in range(size):
            print('{: >4}'.format(sat[(x, y)]), end='')
        print()

def test_sat(serial, n):
    import random
    for _ in range(32):
        s = random.randint(1, 300)
        x = random.randint(1, 300 - s)
        y = random.randint(1, 300 - s)
        print(x,y,s, end='... ')
        actual = power(serial, x, y, s)
        expected = simple_power(serial, x, y, s)
        if actual != expected:
            print("{actual} != {expected}".format(actual=actual, expected=expected))
        else:
            print("{} ✔".format(actual))


def main():
    serial = 1955
    #draw_sat(serial, 20)

    #test_sat(serial, n=32)
    print(max(search(serial=serial)))

main()
