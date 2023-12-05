import re
import sys
from typing import Dict, List, TextIO, Tuple


class Map:
    def __init__(self, target: str) -> None:
        self.target = target
        self.ranges = []
    
    def get(self, i: int) -> int:
        for r, d in self.ranges:
            if i in r:
                return i + d
        return i


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
    tmp = m.get(value)
    #print(source, value, '->', m.target, tmp)
    return lookup(m.get(value), maps, m.target)

    
seeds, maps = parse(sys.stdin)
low = min(lookup(seed, maps) for seed in seeds)
print(low)
