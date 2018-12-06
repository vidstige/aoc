from collections import defaultdict
from string import ascii_lowercase

def load(filename):
    with open('input/{}'.format(filename)) as f:
        
        return [tuple(int(c) for c in line.split(',')) for line in f]

def manhattan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

def infinite(p, rectangle):
    x, y = p
    xmin, ymin, xmax, ymax = rectangle
    if x == xmin or x == xmax:
        return True
    if y == ymin or y == ymax:
        return True
    return False

def rangex(rectangle):
    xmin, _, xmax, _ = rectangle
    return range(xmin - 300, xmax + 300)

def rangey(rectangle):
    _, ymin, _, ymax = rectangle
    return range(ymin - 300, ymax + 300)

def draw(closest, rectangle):
    for y in rangey(rectangle):
        for x in rangex(rectangle):
            c = closest.get((x, y))
            print(ascii_lowercase[c] if c is not None else '.', end='')
        print()

points = load('6')
rectangle = (
    min(x for x, y in points),
    min(y for x, y in points),
    max(x for x, y in points),
    max(y for x, y in points))

closest = {}
for x in rangex(rectangle):
    for y in rangey(rectangle):
        pc = x, y
        distances = sorted([(manhattan(p, pc), i) for i, p in enumerate(points)])
        first = distances[0]
        second = distances[1]
        #print(pc, distances)
        # skip tie distances
        if first[0] < second[0]:
            closest[pc] = first[1]

#draw(closest, rectangle)

counter = defaultdict(int)
for c in closest.values():
    counter[c] += 1

print(counter)
non_infinite = [c for c in counter if not infinite(points[c], rectangle)]
#best = max(non_infinite, key=counter.get)
#print(best, counter[best])
for i in sorted(counter, key=counter.get, reverse=True):
    print(i, counter[i])