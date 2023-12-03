import sys
from typing import Dict, Iterable, Tuple

def parse_grid():
    grid = {}
    for y, line in enumerate(sys.stdin):
        for x, character in enumerate(line.rstrip()):
            grid[(x, y)] = character
    return grid

def neighbors(p: Tuple[int, int]) -> Iterable[Tuple[int, int]]:
    x, y = p
    yield x - 1, y - 1
    yield x, y - 1
    yield x + 1, y - 1
    yield x - 1, y
    #yield x, y
    yield x + 1, y
    yield x - 1, y + 1
    yield x, y + 1
    yield x + 1, y + 1
    

def is_symbol(character: str) -> bool:
    return not character.isdigit() and character != '.'


def numbers(grid: Dict[Tuple[int, int], str]) -> Iterable[Tuple[Tuple[int, int], int]]:
    for y in range(min(ys), max(ys) + 1):
        start_x = None
        for x in range(min(xs), max(xs) + 2):
            p = x, y
            if grid.get(p, '.').isdigit():
                if start_x is None:
                    start_x = x
            elif start_x is not None:
                yield (start_x, x), y
                start_x = None


def get_value(grid: Dict[Tuple[int, int], str], indices: Tuple[Tuple[int, int], int]) -> int:
    (start_x, stop_x), y = indices
    return int(''.join(grid[(x, y)] for x in range(start_x, stop_x)))


grid = parse_grid()
xs = [x for x, _ in grid.keys()]
ys = [y for _, y in grid.keys()]

# first star
def parts(grid: Dict[Tuple[int, int], str]) -> Iterable[int]:
    for (start_x, stop_x), y in numbers(grid):
        number = get_value(grid, start_x, stop_x, y)
        # get all neigbours (including the digits)
        ns = set().union(*(neighbors((x, y)) for x in range(start_x, stop_x)))
        is_part = any(is_symbol(grid.get(n, '.')) for n in ns)
        if is_part:
            yield number

#print(sum(parts(grid)))


# second start
all_numbers = list(numbers(grid))
total = 0
for p, character in grid.items():
    if character == '*':
        ns = set(neighbors(p))
        # find all adjacent numbers
        adjacent = []
        for (start_x, stop_x), y in all_numbers:
            if any((x, y) in ns for x in range(start_x, stop_x)):
                adjacent.append(((start_x, stop_x), y))
            
        if len(adjacent) == 2:
            # gear found
            first, second = adjacent
            gear_ratio = get_value(grid, first) * get_value(grid, second)
            total += gear_ratio
print(total)

