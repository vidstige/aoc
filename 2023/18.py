import re
import sys
from typing import Iterable, List, Sequence, TextIO, Tuple

HLine = Tuple[range, int]
VLine = Tuple[int, range]
Position = Tuple[int, int]

def parse(f: TextIO) -> Tuple[str, int]:
    PATTERN = r'([RLDU]) (\d+) \((#[0-9a-f]{6})\)'
    for line in f:
        match = re.match(PATTERN, line)
        if match:
            direction, count, color = match.groups()
            yield direction, int(count)

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

def dig(lines: Tuple[List[HLine], List[VLine]]) -> Iterable[Position]:
    hlines, vlines = lines
    for xr, y in hlines:
        for x in xr:
            yield x, y
    for x, yr in vlines:
        for y in yr:
            yield x, y

def fill(lines: Tuple[List[HLine], List[VLine]]) -> Iterable[Position]:
    hlines, vlines = lines
    # dig again to get bbox
    perimeter = set(dig(lines))
    xs = [x for x, _ in perimeter]
    xmin, xmax = min(xs), max(xs)
    ys = [y for _, y in perimeter]
    ymin, ymax = min(ys), max(ys)
    for y in range(ymin, ymax + 1):
        inside = False
        x = xmin
        while x < xmax + 2: # 2 for debbuging
            # check horizontal lines
            for xr, ly in hlines:
                if y == ly and x in xr:
                    yr_start = next(yr for lx, yr in vlines if lx in (xr.start, xr.stop) and yr.start == y)
                    yr_stop = next(yr for lx, yr in vlines if lx in (xr.start, xr.stop) and yr.stop == y)
                    if yr_start.step != yr_stop.step:
                        inside = not inside
                    x = max(xr.start, xr.stop) # skip ahead
            # check all vertical lines
            for lx, yr in vlines:
                if x == lx and y in yr:
                    inside = not inside

            if inside and (x, y) not in perimeter:
                yield (x, y)
            x += 1

def print_area(perimeter: Iterable[Position], interior: Iterable[Position]):
    xs = [x for x, _ in perimeter]
    xmin, xmax = min(xs), max(xs)
    ys = [y for _, y in perimeter]
    ymin, ymax = min(ys), max(ys)
    print(xmin, ymin)
    print(xmax + 1, ymax + 1)
    for y in range(ymin - 1, ymax + 2):
        for x in range(xmin - 1, xmax + 2):
            is_perimeter = (x, y) in perimeter
            is_interior = (x, y) in interior
            if is_perimeter and is_interior:
                print('O', end='')
            elif is_perimeter:
                print('X', end='')
            elif is_interior:
                print('#', end='')
            else:
                print('.', end='')
        print()

instructions = list(parse(sys.stdin))
lines = as_lines(instructions)
perimeter = set(dig(lines))
interior = set(fill(lines))
print_area(perimeter, interior)
print(len(perimeter) + len(interior))
