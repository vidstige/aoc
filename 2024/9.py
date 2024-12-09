import sys
import typing

Disk = list[tuple[int | None, int]]

def parse(f: typing.TextIO) -> Disk:
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

def defrag(disk: list[int | None]):
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


disk = parse(sys.stdin)
edisk = expand(disk)
print(format_disk(edisk))
defrag(edisk)
print(format_disk(edisk))
print(checksum(edisk))