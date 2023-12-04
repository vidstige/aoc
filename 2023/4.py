import sys
import re
from typing import List, Set

def parse(f):
    PATTERN = r'Card\s+(\d+): ([^|]*)\|(.*)'
    for i, line in enumerate(f):
        match = re.match(PATTERN, line)
        if not match:
            print('bad line:', line.rstrip())
            continue
        card_id, numbers, winners = match.groups()
        assert int(card_id) - 1 == i

        yield (
            set(int(number) for number in numbers.split()),
            set(int(winner) for winner in winners.split()),
        )


def value(matches: int) -> int:
    if matches == 0:
        return 0
    return 2 ** (matches - 1)


def matching(numbers, winners) -> int:
    return sum(1 for number in numbers if number in winners)

cards = list(parse(sys.stdin))
matches = [matching(numbers, winners) for numbers, winners in cards]

# first star
print(sum(value(m) for m in matches))

# second star
def count(matches: List[int]):
    n = len(matches)
    copies = [1] * n
    for i, m in enumerate(matches):
        for j in range(i + 1, i + m + 1):
            copies[j] += copies[i]
    return sum(copies)

print(count(matches))