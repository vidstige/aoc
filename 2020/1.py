from itertools import product
from functools import reduce
import operator
import sys

def multiply(iterable):
    return reduce(operator.mul, iterable, 1)

items = [int(row) for row in sys.stdin.readlines()]
matching = next(multiply(i) for i in product(items, items, items) if sum(i) == 2020)
print(matching)

