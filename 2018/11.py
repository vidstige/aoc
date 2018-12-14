from tqdm import tqdm
from functools import lru_cache

def hundreds(x):
    return int(str(x // 100)[-1])


def cell(serial, p):
    x, y = p
    rack_id = x + 10
    level = (rack_id * y + serial) * rack_id
    return hundreds(level) - 5


def grid(w, h):
    for y in range(w):
        for x in range(h):
            yield x, y

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

def search():
levels = {}
power_grid = compute_power_grid(serial=1955)
size = 300
for kernel in tqdm(range(1, 300 + 1)):
    left = kernel // 2
    right = kernel - left
    for a, b in grid(size - kernel, size - kernel):
        x, y = a + 1, b + 1
        print(x, y, kernel)
    
#power_levels(levels, power_grid, 3)
#print(highest(levels))
