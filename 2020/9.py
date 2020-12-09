import sys
from itertools import combinations

preamble = 25
sequence = [int(line) for line in sys.stdin.readlines()]

active = sequence[:preamble]
for n in sequence[preamble:]:
    valid = set(i + j for i, j in combinations(active, 2))
    if n not in valid:
        print(n)

    active.pop(0)
    active.append(n)
