import re
import sys
from typing import Dict, Iterable, List, TextIO, Tuple, TypeVar


def range_overlap(a: range, b: range) -> range:
    return range(max(a.start, b.start), min(a.stop, b.stop))


def contains(a: range, b: range) -> bool:
    """Whether a completely contains b"""
    return b.start in a and b.stop in a


def range_remove(a: range, b: range) -> Iterable[range]:
    """removes b from the range a, yielding zero, one or to two ranges"""
    # TODO: skip empty intervals
    if contains(a, b):
        # range is split into two parts
        yield range(a.start, b.start)
        yield range(b.stop, a.stop)
    else:
        # check for left/right overlaps
        if b.start in a:
            yield range(a.start, b.start)
        if b.stop - 1 in a:
            yield range(b.stop, a.stop)


class Map:
    def __init__(self, target: str) -> None:
        self.target = target
        self.ranges: List[Tuple[range, int]] = []

    def get(self, i: int) -> int:
        for r, d in self.ranges:
            if i in r:
                return i + d
        return i
    
    def get_range(self, key: range) -> Iterable[range]:
        """Maps input range into one or more ranges."""
        todo = [key]  # ranges left to check
        result = []  # mapped ranges
        while todo:
            a = todo.pop()  # take any range
            dirty = False
            for b, delta in self.ranges:
                # find overlapp
                overlap = range_overlap(a, b)
                if overlap:
                    dirty = True
                    result.append(range(overlap.start + delta, overlap.stop + delta))

                # add all non-empty ranges as todos
                splits = [r for r in range_remove(a, b) if r]
                #print(a, '-', b, '=', splits)
                if splits:
                    # add splits
                    #print('  ', a, b, ' -> ', splits)
                    todo.extend(splits)
                    dirty |= bool(range_overlap(b, a))
                    break

            if not dirty:
                # use default value
                #print('default needed for', a)
                result.append(a)

        # make sure the number of output equals the number of inputs
        assert sum(len(r) for r in result) == len(key)
        return result

    def __repr__(self) -> str:
        return f"Map({self.target}, {self.ranges})"


def parse(f: TextIO) -> Tuple[List[int], Dict[str, Map]]:
    SEEDS_PATTERN = r'seeds: (.*)'
    MAP_PATTERN = r'(.*)-to-(.*) map:'
    seeds = []
    maps: Dict[str, Map] = {}
    source = None
    for line in f:
        if not line.strip():
            continue
        match = re.match(SEEDS_PATTERN, line)
        if match:
            seeds = [int(seed) for seed in match.group(1).split()]
            continue
        match = re.match(MAP_PATTERN, line)
        if match:
            source, target = match.group(1), match.group(2)
            maps[source] = Map(target)
            continue
        target_start, source_start, length = [int(p) for p in line.split()]
        source_range = range(source_start, source_start + length)
        delta = target_start - source_start
        maps[source].ranges.append((source_range, delta))
    return seeds, maps


def lookup(value: int, maps: Dict[str, Map], source: str = 'seed') -> int:
    m = maps.get(source)
    if m is None:
        assert source == 'location'
        return value
    print(source, '->', m.target, ':', value, '->', m.get(value))
    return lookup(m.get(value), maps, m.target)


T = TypeVar('T')
def pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T, T]]:
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


seeds, maps = parse(sys.stdin)
# first star
low = min(lookup(seed, maps) for seed in seeds)
print(low)

# second star
def search(rs: range, maps: Dict[str, Map], source: str = 'seed') -> int:
    m = maps.get(source)
    if m is None:
        assert source == 'location'
        return min(r.start for r in rs)
    
    print(source, '->', m.target, ':', rs)
    return min(search(m.get_range(r), maps, m.target) for r in rs)


minseeds = []
seed_ranges = [range(start, start + length) for start, length in pairwise(seeds)]
low = min(search([r], maps) for r in seed_ranges)
print(low)
