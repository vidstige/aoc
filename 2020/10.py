from collections import Counter
from itertools import groupby
import sys

def choices(route):
    pass

adapters = [int(line) for line in sys.stdin.readlines()]
route = list(sorted([0] + adapters + [max(adapters) + 3]))
diffs = [b - a for a, b in zip(route[:-1], route[1:])]
counts = Counter(diffs)
print(counts)
print(diffs)
from math import factorial
def noverp(n, r):
    return factorial(n) // factorial(r) // factorial(n - r)

def combinations(n):
    for p in range(0, n):
        print(p, 'från', n, noverp(n-1, p))
    return sum(noverp(n-1, p) for p in range(0, min(n, 3)))

x = 1
for a, b in groupby(diffs):
    bb = list(b)
    if a == 1 and len(bb) > 1:
        x *= combinations(len(bb))
print(x)
