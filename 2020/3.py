import sys

def parse(f):
    return [line.strip() for line in f]

trees = parse(sys.stdin)
print(trees)
x, y = 0, 0
slope = 3, 1
n = 0
while y < len(trees):
    if trees[y][x % len(trees[y])] == '#':
        n += 1
    x, y = x + slope[0], y + slope[1]
print(n)
        
