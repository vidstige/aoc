from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
import sys

Position = tuple[int, int]

@dataclass
class BBox:
    xmin: int
    ymin: int
    xmax: int
    ymax: int

    def __contains__(self, position: Position) -> bool:
        x, y = position
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax

        
    @staticmethod
    def from_positions(positions: list[Position]) -> 'BBox':
        xmin, ymin = min(positions)
        xmax, ymax = max(positions)
        return BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)


def parse(f):
    grid = defaultdict(list)
    positions = []
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            p = x, y
            if c != '.':
                grid[c].append(p)
            positions.append(p)
    
    return dict(grid), BBox.from_positions(positions)


def sub(a: Position, b: Position) -> Position:
    ax, ay = a
    bx, by = b
    return ax - bx, ay - by

def add(a: Position, b: Position) -> Position:
    ax, ay = a
    bx, by = b
    return ax + bx, ay + by


def find_antinodes(nodes: list[Position], octaves=None):
    for a, b in combinations(nodes, r=2):
        p, i = a, 0
        while p in bbox:
            if octaves is None or i in octaves:
                yield p
            p, i = add(p, sub(a, b)), i + 1
        p, i = b, 0
        while p in bbox:
            if octaves is None or i in octaves:
                yield p
            p, i = add(p, sub(b, a)), i + 1


grid, bbox = parse(sys.stdin)
antinodes_0, antinodes_1 = set(), set()
for frequency, nodes in grid.items():
    for antinode in find_antinodes(nodes, octaves=[1]):
        antinodes_0.add(antinode)

    for antinode in find_antinodes(nodes):
        antinodes_1.add(antinode)


print(len(antinodes_0))
print(len(antinodes_1))