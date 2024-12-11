from functools import cache
import sys

@cache
def single(stone: int, n: int) -> int:
    if n == 0:
        return 1
    if stone == 0:
        return single(1, n - 1)
    decimal = str(stone)
    if len(decimal) % 2 == 0:
        mid = len(decimal) // 2
        left = int(decimal[:mid])
        right = int(decimal[mid:])
        return single(left, n - 1) + single(right, n - 1)
    return single(stone * 2024, n - 1)

def blink(stones: list[int], n: int) -> int:
    return sum(single(stone, n) for stone in stones)

stones = [int(stone) for stone in sys.stdin.read().split()]
print(blink(stones, n=75))
