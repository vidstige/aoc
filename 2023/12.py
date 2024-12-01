import sys
from typing import Iterable, List, TextIO, Tuple


def parse(f: TextIO) -> Iterable[Tuple[str, List[int]]]:
    for line in f:
        conditions, raw_records = line.split()
        records = [int(r) for r in raw_records.split(',')]
        yield conditions, records


def with_condition(conditions: str, condition: str, index: int) -> str:
    return conditions[:index] + condition + conditions[index + 1:]

def search(conditions: str, index: int, records: List[int], ri: int, r: int) -> int:
    if ri >= len(records):
        # everything is checked! Make sure the rest of the springs are working (or unknown)
        if all(c != '#' for c in conditions[index:]):
            #print('  ok', conditions)
            return 1
        return 0
    if index >= len(conditions):
        # if we've still got records, but no conditions it's an inconsistency
        if records[ri] == r and ri == len(records) - 1:
            #print('  ok', conditions)
            return 1
        return 0
    
    condition = conditions[index]
    record = records[ri]
    if record == r:
        # when this record is done, the current spring is expected to be working
        if condition == '#':
            return 0
        return search(with_condition(conditions, '.', index), index + 1, records, ri + 1, 0)

    # continue search if damaged or working
    if condition == '#':
        return search(conditions, index + 1, records, ri, r + 1)
    if condition == '.':
        if r > 0 and r < record:
            return 0
        return search(conditions, index + 1, records, ri, 0)

    # condition is unkown. Branch out search
    damaged = search(with_condition(conditions, '#', index), index, records, ri, r)
    working = search(with_condition(conditions, '.', index), index, records, ri, r)
    return working + damaged

def wrapper(row: Tuple[str, List[int]]) -> int:
    print('.')
    conditions, records = row
    return search(conditions, 0, records, 0, 0)

def unfold(row: Tuple[str, List[int]], n: int = 5) -> Tuple[str, List[int]]:
    conditions, records = row
    return '?'.join([conditions] * n), records * n

data = list(parse(sys.stdin))

# first star
print(sum(wrapper(row) for row in data))

# second star
print(sum(wrapper(unfold(row)) for row in data))
