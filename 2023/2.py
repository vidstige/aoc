import math
import sys
import re
from typing import Dict, Iterable, List, Tuple


def parse_draw(draw: str) -> Dict[str, int]:
    result = {}
    for cube in draw.split(','):
        count, color = cube.split()
        result[color.strip()] = int(count)
    return result


def parse() -> Tuple[int, List[Dict[str, int]]]:
    PATTERN = 'Game (\d+): (.*)'
    for line in sys.stdin:
        match = re.match(PATTERN, line)
        if match:
            game_id, rest = match.groups()
            draws = [parse_draw(draw) for draw in rest.split(';')]
            yield int(game_id), draws

pool = {'red': 12, 'green': 13, 'blue': 14}
def ok(draw: Dict[str, int]) -> bool:
    return all(value <= pool[color] for color, value in draw.items())

games = list(parse())

# first star
total = 0
for game_id, draws in games:
    if all(ok(draw) for draw in draws):
        total += game_id
print(total)

# second star
power = 0
for game_id, draws in games:
    colors = set().union(*(draw.keys() for draw in draws))
    cubes = {color: max(draw.get(color, 0) for draw in draws) for color in colors}
    power += math.prod(cubes.values())

print(power)