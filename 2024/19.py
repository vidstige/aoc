from functools import cache
import sys
from typing import TextIO

def parse(f: TextIO):
    towels = [towel.strip() for towel in f.readline().split(',')]
    f.readline()  # blank
    patterns = [line.rstrip() for line in f]
    return towels, patterns

towels, patterns = parse(sys.stdin)

@cache
def search(pattern: str) -> int:
    if not pattern:
        return 1
    return sum(search(pattern[len(towel):]) for towel in towels if pattern.startswith(towel))


print(sum(1 for pattern in patterns if search(pattern) > 0))
