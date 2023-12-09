import sys
from typing import Iterable, List, TextIO


def parse(f: TextIO) -> Iterable[List[int]]:
    for line in f:
        yield [int(part) for part in line.split()]


def diff(values: List[int]) -> List[int]:
    return [second - first for first, second in zip(values, values[1:])]


def extrapolate(values: List[int]) -> int:
    assert values, "Can't extrapolate empty values"
    if all(v == 0 for v in values):
        return 0
    return values[-1] + extrapolate(diff(values))

total = sum(extrapolate(history) for history in parse(sys.stdin))
print(total)
    