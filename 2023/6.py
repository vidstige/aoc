import math
import sys
from typing import List, TextIO

def parse_ints(f: TextIO, header: str) -> List[int]:
    parts = sys.stdin.readline().split()
    assert header in parts[0]
    return [int(d) for d in parts[1:]]


def ways_to_win(time: int, distance: int) -> int:
    return sum(1 for hold in range(1, time) if hold * (time - hold) > distance)


def unkern(numbers: List[int]) -> int:
    return int(''.join(str(n) for n in numbers))

times = parse_ints(sys.stdin, 'Time')
distances = parse_ints(sys.stdin, 'Distance')

# first start
ways = [ways_to_win(time, distance) for time, distance in zip(times, distances)]
print(math.prod(ways))

# second start
print(ways_to_win(unkern(times), unkern(distances)))
