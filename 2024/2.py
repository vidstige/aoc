import sys

def is_increasing(diff: int) -> bool:
    return diff > 0

def is_decreasing(diff: int) -> bool:
    return diff < 0

a = []
for line in sys.stdin:
    levels_original = [int(level) for level in line.split()]
    any_safe = False
    for skip in range(len(levels_original)):
        levels = levels_original.copy()
        del levels[skip]

        diffs = [b - a for a, b in zip(levels, levels[1:])]
        safe = (
            all(is_increasing(diff) for diff in diffs) or
            all(is_decreasing(diff) for diff in diffs)
        ) and (
            all(abs(diff) >= 1 and abs(diff) <= 3 for diff in diffs)
        )
        any_safe = any_safe or safe
    #print(levels, any_safe)
    a.append(any_safe)

print(sum(1 for safe in a if safe))
