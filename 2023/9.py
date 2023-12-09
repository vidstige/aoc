import sys
from typing import Iterable, List, TextIO


def parse(f: TextIO) -> Iterable[List[int]]:
    for line in f:
        yield [int(part) for part in line.split()]


def diff(values: List[int]) -> List[int]:
    return [second - first for first, second in zip(values, values[1:])]


def forward(values: List[int]) -> int:
    assert values, "Can't extrapolate empty values"
    if all(v == 0 for v in values):
        return 0
    return values[-1] + forward(diff(values))

history = list(parse(sys.stdin))
total = sum(forward(values) for values in history)
print(total)


def backwards(values: List[int]) -> int:
    assert values, "Can't extrapolate empty values"
    if all(v == 0 for v in values):
        return 0
    return values[0] - backwards(diff(values))

print(sum(backwards(history) for history in history))
