import re
import sys
from typing import Counter, Iterable, Sequence, TextIO

Vector = tuple[int, int]
Robot = tuple[Vector, Vector]

def parse(f: TextIO) -> Iterable[Robot]:
    for line in f:
        match = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line)
        x, y, vx, vy = [int(g) for g in match.groups()]
        yield (x, y), (vx, vy)


def positions_after(robots: Iterable[Robot], w: int, h: int, n: int) -> Iterable[Vector]:
    for (x, y), (vx, vy) in robots:
        yield (x + n * vx) % w, (y + n * vy) % h

def product(items: Iterable[int]) -> int:
    p = 1
    for item in items:
        p *= item
    return p

def quadrant(position: Vector, mid: Vector) -> tuple[bool | None, bool | None]:
    x, y = position
    mx, my = mid
    if x == mx or y == my:
        return None
    return x < mx, y < my
                                  
def quadrants(positions: Iterable[Vector], w: int, h: int):
    mid = w//2, h//2
    q = Counter(quadrant(p, mid) for p in positions)
    q.pop(None)
    return q.values()

def print_grid(positions: Sequence[Vector], w: int, h: int) -> None:
    for y in range(h):
        print(''.join('@' if (x, y) in positions else '.' for x in range(w)))
            

with open(sys.argv[1]) as f:
    robots = list(parse(f))

#w, h = 11, 7
w, h = 101, 103
positions = positions_after(robots, w, h, 100)
print(product(quadrants(positions, w, h)))

for i in range(4000, 8000):
    positions = positions_after(robots, w, h, i)
    print
    print(i)
    print_grid(list(positions), w, h)
    input()