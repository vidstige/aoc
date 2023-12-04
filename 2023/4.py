import sys
import re
from typing import Set

def parse(f):
    PATTERN = r'Card\s+(\d+): ([^|]*)\|(.*)'
    for line in f:
        match = re.match(PATTERN, line)
        if not match:
            print(line)
            continue
        card_id, numbers, winners = match.groups()
        
        yield (
            int(card_id),
            set(int(number) for number in numbers.split()),
            set(int(winner) for winner in winners.split()),
        )


def value(numbers: Set[int], winners: Set[int]) -> int:
    count = sum(1 for number in numbers if number in winners)
    if count == 0:
        return 0
    return 2 ** (count - 1)

print(sum(value(numbers, winners) for _, numbers, winners in parse(sys.stdin)))
