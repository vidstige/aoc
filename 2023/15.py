import sys
from typing import Iterable, TextIO

def parse(f: TextIO) -> Iterable[str]:
    for line in sys.stdin:
        yield from line.rstrip().split(',')

def ascii_hash(s: str) -> int:
    h = 0
    for c in s:
        h = ((h + ord(c)) * 17) & 0xff
    return h

print(sum(ascii_hash(s) for s in parse(sys.stdin)))
