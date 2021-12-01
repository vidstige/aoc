from itertools import product
from functools import reduce
import operator
import sys


def sliding_sum(xs, k):
    window = []
    result = []
    for x in xs:
        window.append(x)
        window = window[-k:]
        if len(window) == k:
            result.append(sum(window))
    return result
    
depths = [int(row) for row in sys.stdin.readlines()]
summed = sliding_sum(depths, 3)
deltas = [a - b for a, b in zip(summed[1:], summed[:-1])]
n = len([1 for d in deltas if d > 0])
print(n)
