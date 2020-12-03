import sys

def parse(f):
    return [line.strip() for line in f]

def count(trees, slope):
    x, y = 0, 0
    n = 0
    while y < len(trees):
        if trees[y][x % len(trees[y])] == '#':
            n += 1
        x, y = x + slope[0], y + slope[1]
    return n

trees = parse(sys.stdin)
slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]
p = 1
for slope in slopes:
    p *= count(trees, slope)
print(p)
        
