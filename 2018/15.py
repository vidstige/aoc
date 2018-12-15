from typing import Iterable, List, Set, Tuple

Position = Tuple[int, int]


def rev(t: tuple) -> tuple:
    return tuple(reversed(t))


class Unit(object):
    def __init__(self,
            team: str,
            position: Position,
            hp: int=200, ap: int=3):
        self.team = team
        self.p = position
        self.hp = hp
        self.ap = ap

def load(filename):
    cave = set()
    units = []
    with open(filename) as f:
        for y, line in enumerate(f):
            for x, char in enumerate(line):
                p = x, y
                if char == '#':
                    cave.add(p)
                if char in 'EG':
                    units.append(Unit(team=char, position=p))
    return cave, units

def range_x(cave: Set[Position]) -> range:
    xmin = min(x for x, _ in cave)
    xmax = max(x for x, _ in cave)
    return range(xmin, xmax + 1)

def range_y(cave: Set[Position]) -> range:
    ymin = min(y for _, y in cave)
    ymax = max(y for _, y in cave)
    return range(ymin, ymax + 1)

def draw(cave: Set[Position], units: List[Unit]) -> None:
    print('BATTLE')
    for y in range_y(cave):
        for x in range_x(cave):
            p = x, y
            unit = next((u for u in units if u.p == p), None)
            if unit:
                print(unit.team, end='')
            else:
                print('#' if p in cave else ' ', end='')
        print()

def main():
    cave, units = load('input/15ex0')
    draw(cave, units)

main()
