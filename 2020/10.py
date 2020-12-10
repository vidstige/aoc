from collections import Counter
import sys

adapters = [int(line) for line in sys.stdin.readlines()]
route = list(sorted([0] + adapters + [max(adapters) + 3]))
diffs = (b - a for a, b in zip(route[:-1], route[1:]))
counts = Counter(diffs)

print(counts)