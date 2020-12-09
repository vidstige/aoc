import sys
from itertools import combinations


def invalid(sequence, preamble):
    active = sequence[:preamble]
    for n in sequence[preamble:]:
        valid = set(i + j for i, j in combinations(active, 2))
        if n not in valid:
            yield n
        active.pop(0)
        active.append(n)


def search(sequence, n):
    for a in range(len(sequence) - 2):
        for b in range(a + 2, len(sequence)):
            if sum(sequence[a:b]) == n:
                print(sequence[a], sequence[b - 1],
                    min(sequence[a:b]) + max(sequence[a:b]))


preamble = 25
sequence = [int(line) for line in sys.stdin.readlines()]
invalid_number = next(invalid(sequence, preamble))

search(sequence, invalid_number)
