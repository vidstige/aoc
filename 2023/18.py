from collections import Counter, OrderedDict, defaultdict
import re
import sys
from typing import Dict, Iterable, List, Sequence, Set, TextIO, Tuple

Position = Tuple[int, int]

def parse(f: TextIO) -> Iterable[Tuple[str, int, str]]:
    PATTERN = r'([RLDU]) (\d+) \((#[0-9a-f]{6})\)'
    for line in f:
        match = re.match(PATTERN, line)
        if match:
            direction, count, color = match.groups()
            yield direction, int(count), color


def first_star(instructions: Sequence[Tuple[str, int, str]]) -> Sequence[Tuple[str, int]]:
    for direction, count, _ in instructions:
        yield direction, count

def second_star(instructions: Sequence[Tuple[str, int, str]]) -> Sequence[Tuple[str, int]]:
    raise NotImplemented()

HLine = Tuple[range, int]
VLine = Tuple[int, range]
def as_lines(instructions: Iterable[Tuple[str, int]], start: Position = (0, 0)) -> Tuple[List[HLine], List[VLine]]:
    hlines, vlines = [], []
    p = start
    for direction, count in instructions:
        x, y = p
        if direction == 'R':
            hlines.append((range(x, x + count), y))
            p = x + count, y
        if direction == 'L':
            hlines.append((range(x, x - count, -1), y))
            p = x - count, y
        if direction == 'D':
            vlines.append((x, range(y, y + count)))
            p = x, y + count
        if direction == 'U':
            vlines.append((x, range(y, y - count, -1)))
            p = x, y - count
    return hlines, vlines

def all_positions(boxes: Tuple[range, range]) -> Iterable[Position]:
    for xr, yr in boxes:
        for x in range(xr.start, xr.stop + 1):
            for y in yr:
                yield x, y

def xor_rangesets(ars: List[range], brs: List[range]) -> List[range]:
    # a: ------      -----      ----  --       --     --------
    # b: --  --      ---                  --     --      ---  
    # c:   --           ---     ----  --  --   ----   ---   --
    vertices = defaultdict(int)
    for r in ars + brs:
        vertices[r.start] += 1
        vertices[r.stop] += 1
    start = None
    result = []
    for x, c in sorted(vertices.items()):
        assert c in (1, 2)
        if c == 1:
            if start is not None:
                result.append(range(start, x))
                start = None
            else:
                start = x
    return result

def or_rangesets(ars: List[range], brs: List[range]) -> List[range]:
    # a: ------      -----      ----  --       --     --------
    # b: --  --      ---                  --     --      ---  
    # c: ------      ------     ----  --  --   ----   --------
    starts = defaultdict(int)
    stops = defaultdict(int)
    for r in ars + brs:
        if r.step > 0:
            starts[r.start] += 1
            stops[r.stop] += 1
        else:
            starts[r.stop] += 1
            stops[r.start] += 1

    counter = 0
    start = None
    result = []
    for x in sorted(list(starts.keys()) + list(stops.keys())):
        if counter == 0:
            start = x
        counter += starts[x]
        counter -= stops[x]
        if counter == 0:
            if x > start:
                result.append(range(start, x))
            start = None

    return result

def fill(instructions: Iterable[Tuple[str, int]]) -> Iterable[Tuple[range, range]]:
    # 1. Parse into vlines and hlines
    hlines, vlines = as_lines(instructions)
    
    # 2. Compute auxiliary data structures for scanning vertical scanning
    htmp = defaultdict(list)
    for xr, y in hlines:
        htmp[y].append(xr)

    # compress to sorted list
    hlookup = [entry for entry in sorted(htmp.items())]

    row = []  # start with empty rangeset
    y0 = None
    area = 0
    for y1, xrs in hlookup:
        # yield single line block with union
        yr = range(y1, y1 + 1)
        for xr in or_rangesets(xrs, row):
            yield xr, yr
        if y0 is not None:
            yr = range(y0 + 1, y1)
            for xr in row:
                yield xr, yr
        row = xor_rangesets(row, xrs)
        y0 = y1

    # rangeset must be empty after if shape is closed
    assert row == []
    return area

def bbox(positions: Iterable[Position]) -> Tuple[range, range]:
    xmin, xmax = min(x for x, _ in positions), max(x for x, _ in positions)
    ymin, ymax = min(y for _, y in positions), max(y for _, y in positions)
    return range(xmin, xmax + 1), range(ymin, ymax + 1)

def print_grid(grid: Iterable[Position]) -> None:
    xr, yr = bbox(grid)
    counter = Counter(grid)
    for y in yr:
        for x in xr:
            print(counter.get((x, y), '.'), end='')
            #print('#' if (x, y) in grid else '.', end='')
        print()

# test range set operations
# a: ------      -----      ----  --       --     --------
# b: --  --      ---                  --     --      ---  
# c:   --           --      ----  --  --   ----   ---   --
a = [range(6, 12), range(18, 23), range(29, 33), range(35, 37), range(44, 46), range(51, 59)]
b = [range(6, 8), range(10, 12), range(18, 21), range(39, 41), range(46, 48), range(54, 57)]
c = [range(8, 10), range(21, 23), range(29, 33), range(35, 37), range(39, 41), range(44, 48), range(51, 54), range(57, 59)]
assert xor_rangesets(a, b) == c

# a: ------      -----      ----  --       --     --------
# b: --  --      ---                  --     --      ---  
# c: ------      -----      ----  --  --   ----   --------
c = [range(6, 12), range(18, 23), range(29, 33), range(35, 37), range(39, 41), range(44, 48), range(51, 59)]
assert or_rangesets(a, b) == c

instructions = list(parse(sys.stdin))
boxes = fill(first_star(instructions))
grid = list(all_positions(boxes))
assert len(grid) == len(set(grid)), "duplicates!"
#print_grid(grid)
print(len(grid))
