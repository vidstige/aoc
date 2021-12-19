import sys


def parse(line):
    pairs = []
    for c in line:
        if c == '[':
            pairs.append([])
        if c == ']':
            assembled = pairs.pop()
            if pairs:
                pairs[-1].append(assembled)
            else:
                return assembled
        if c.isdigit():
            pairs[-1].append(int(c))


def explode_one(sn, n):
    """Explodes a single snail number at level n"""
    if isinstance(sn, int):
        return sn
    left, right = sn
    if n == 4:
        assert isinstance(left, int)
        assert isinstance(right, int)
        return left, 0, right
    
    return 0, [explode_one(left, n + 1), explode_one(right, n + 1)], 0


for line in sys.stdin:
    sn = parse(line)
    print(sn)
    print(explode_one(sn, n=0))
