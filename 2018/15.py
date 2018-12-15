from typing import Iterable, List, Set, Tuple

Position = Tuple[int, int]


def rev(t: tuple) -> tuple:
    return tuple(reversed(t))


class Unit(object):
    def __init__(self,
            team: str,
            position: Position,
            hp: int=200, attack_power: int=3):
        self.team = team
        self.p = position
        self.hp = hp
        self.attack_power = attack_power

    def is_enemy(self, other) -> bool:
        return self.team != other.team

    def __repr__(self) -> str:
        return '{}({}, {}, {})'.format(
            type(self).__name__,
            self.team,
            self.p,
            self.hp
        )

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
    for y in range_y(cave):
        for x in range_x(cave):
            p = x, y
            unit = next((u for u in units if u.p == p), None)
            if unit:
                print(unit.team, end='')
            else:
                print('#' if p in cave else '.', end='')
        print()

def neighbours(p: Position) -> Iterable[Position]:
    x, y = p
    # reading order
    yield x, y - 1
    yield x - 1, y
    yield x + 1, y
    yield x, y + 1


def free_neighbours(cave: Set[Position], p: Position) -> Iterable[Position]:
    return (n for n in neighbours(p) if n not in cave)


def find_reachable(blocked: Set[Position], start: Position, destinations: Set[Position]) -> Iterable[Position]:
    queue = [(n, 0, n) for n in free_neighbours(blocked, start)]
    visited = set()
    while queue:
        p, d, first = queue.pop(0)
        visited.add(p)
        if p in destinations:
            x, y = p
            yield d, y, x, first
        queue.extend((n, d + 1, first) for n in free_neighbours(blocked, p) if n not in visited)


def round(cave, units):
    # movement
    someone = list(units)
    alive = set(units)
    while someone:
        someone.sort(key=lambda u: rev(u.p))
        unit = someone.pop(0)

        enemy_neighbours = list(u for u in alive if u.p in neighbours(unit.p) and unit.is_enemy(u))
        if not enemy_neighbours:
            # move to New Position
            blocked = cave | set(u.p for u in alive)
            enemy_positions = [u.p for u in alive if unit.is_enemy(u)]
            if not enemy_positions:
                # remove dead units
                for dead in set(units) - alive:
                    units.remove(dead)
                return False
            destinations = []
            for p in enemy_positions:
                destinations.extend(n for n in free_neighbours(blocked, p))
            reachable = list(find_reachable(blocked, unit.p, destinations))
            if reachable:
                r = sorted(reachable)
                unit.p = r[0][-1]
    
        # attack
        # alive unit neighbours
        targets = list(u for u in alive if u.p in neighbours(unit.p) and unit.is_enemy(u))
        # sort by low hp first, reading order second
        targets.sort(key=lambda u: (u.hp, rev(u.p)))
        target = targets[0] if targets else None
        if target:
            # attack target
            target.hp -= unit.attack_power
            if target.hp <= 0:
                alive.remove(target)
                # dead units can't take a turn
                if target in someone:
                    someone.remove(target)

    # remove dead units
    for dead in set(units) - alive:
        units.remove(dead)

    return True

def battle(filename: str):
    cave, units = load(filename)
    i = 0
    #draw(cave, units)
    while round(cave, units):
        i += 1

    #draw(cave, units)
    #for unit in units:
    #    print(unit)
    hp = sum(u.hp for u in units)
    return i, hp

def main():
    print(battle('input/15ex0'), (47, 590))
    print(battle('input/15ex1'), (37, 982))
    print(battle('input/15ex2'), (46, 859))
    print(battle('input/15ex3'), (54, 536))
    print(battle('input/15ex4'), (20, 937))

main()
