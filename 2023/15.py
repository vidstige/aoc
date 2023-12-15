import sys
from typing import Iterable, List, TextIO, Tuple

def parse(f: TextIO) -> Iterable[str]:
    for line in sys.stdin:
        yield from line.rstrip().split(',')

def ascii_hash(s: str) -> int:
    h = 0
    for c in s:
        h = ((h + ord(c)) * 17) & 0xff
    return h

def focusing_power(boxes: List[List[Tuple[str, int]]]) -> int:
    total = 0
    for box_number, box in enumerate(boxes, start=1):
        for slot_number, (_, lens) in enumerate(box, start=1):
            total += box_number * slot_number * lens
    return total

# part 1
data = list(parse(sys.stdin))
print(sum(ascii_hash(s) for s in data))

# part 2
boxes = [[] for _ in range(256)]
for s in data:
    if '=' in s:
        replace, lens_raw = s.split('=')
        hashed = ascii_hash(replace)
        lens = int(lens_raw)
        # find index of this label
        index = next((i for i, (label, _) in enumerate(boxes[hashed]) if label == replace), None)
        if index is None:
            boxes[hashed].append((replace, lens))
        else:
            boxes[hashed][index] = (replace, lens)
        
    if s.endswith('-'):
        remove = s[:-1]
        hashed = ascii_hash(remove)
        # remove all labels in hashed box
        boxes[hashed] = [(label, lens) for label, lens in boxes[hashed] if label != remove]

    print('After', s)
    for index, box in enumerate(boxes):
        if box:
            print(f'Box {index}: {box}')

print(focusing_power(boxes))