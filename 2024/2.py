import sys

def is_increasing(diff: int) -> bool:
    return diff > 0

def is_decreasing(diff: int) -> bool:
    return diff < 0

reports = []
for line in sys.stdin:
    levels = [int(level) for level in line.split()]
    diffs = [b - a for a, b in zip(levels, levels[1:])]
    safe = (
        all(is_increasing(diff) for diff in diffs) or
        all(is_decreasing(diff) for diff in diffs)
    ) and (
        all(abs(diff) >= 1 and abs(diff) <= 3 for diff in diffs)
    )
    print(levels, safe)
    reports.append(safe)

print(sum(1 for safe in reports if safe))
