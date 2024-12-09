import sys
from typing import Callable, TextIO

Disk = list[tuple[int | None, int]]

def parse(f: TextIO) -> Disk:
    line = f.readline().rstrip()
    disk = []
    for i, c in enumerate(line):
        file_id = i // 2 if i % 2 == 0 else None
        size = int(c)
        disk.append((file_id, size))
    return disk

def expand(disk: Disk) -> list[int | None]:
    expanded = []
    for file_id, size in disk:
        expanded.extend([file_id] * size)
    return expanded

def fragment(disk: list[int | None]):
    end = len(disk) - 1
    start = disk.index(None)  # find first free
    while start <= end:
        # swap index and end
        disk[end], disk[start] = disk[start], disk[end]
        start = disk.index(None, start)  # find first free
        end -= 1

def checksum(disk: list[int | None]) -> int:
    return sum(file_id * position for position, file_id in enumerate(disk) if file_id)

def format_disk(disk: list[int | None]) -> str:
    return ''.join(str(sector) if sector is not None else '.' for sector in disk)


def defrag(disk: Disk):
    file_ids = sorted((file_id, size) for file_id, size in disk if file_id is not None)
    file_ids.reverse()
    for file_id, size in file_ids:
        free_index = next((i for i, (fid, free) in enumerate(disk) if fid is None and free >= size), None)
        if free_index is not None:
            # find index
            index = next(i for i, (fid, _) in enumerate(disk) if fid == file_id)
            
            # stop if we would start moving right
            if free_index > index:
                continue

            # reduce size
            assert disk[free_index][0] is None
            disk[free_index] = (disk[free_index][0], disk[free_index][1] - size)

            # insert file 
            disk[index] = (None, disk[index][1])
            disk.insert(free_index, (file_id, size))

disk = parse(sys.stdin)
# 1
edisk = expand(disk)
print(format_disk(edisk))
fragment(edisk)
print(checksum(edisk))
# 2
defrag(disk)
#print(format_disk(expand(disk)))
print(checksum(expand(disk)))

# too low: 6344673854800