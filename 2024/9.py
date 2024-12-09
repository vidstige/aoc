import sys
import typing

def parse(f: typing.TextIO):
    line = f.readline().rstrip()
    disk = []
    for i, c in enumerate(line):
        if i % 2 == 0:
            file_id = i // 2
            size = int(c)
            disk.extend([file_id] * size)
        else:
            size = int(c)
            disk.extend([None] * size)
    return disk

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
print(format_disk(disk))
defrag(disk)
print(format_disk(disk))
print(checksum(disk))