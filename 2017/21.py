PATTERN = """.#.
..#
###"""

def valid(block):
    for y, row in enumerate(block):
        if len(row) != len(block):
            raise ValueError("Bad block: Row {} has {} columns, but should be {}".format(y, len(row), len(block)))
    return block

def fmt(grid):
    return "\n".join(grid)


def chunk(grid, s):
    """Splits the 2d grid in to s-by-s blocks"""
    n = len(grid) // s
    for y in range(n):
        for x in range(n):
            yield valid([grid[y*s+i][x*s:x*s+s] for i in range(s)])


def stitch(blocks, s):
    grid = []
    n = 0
    for i, block in enumerate(blocks):
        for dy, row in enumerate(block):
            y = (i // s) * len(block) + dy
            while len(grid) <= y:
                grid.append('')
            grid[y] += row
    return valid(grid)


def match(block, pattern):
    if len(block) != len(pattern):
        return False

    bs = len(block)
    # flips
    o = True
    h = True
    v = True
    vh = True
    # rotations
    r090 = True
    r270 = True
    r180 = True
    hmm = True

    for y in range(bs):
        for x in range(bs):
            b = block[y][x]

            o &= b == pattern[y][x]
            h &= b == pattern[bs-1-y][x]
            v &= b == pattern[y][bs-1-x]
            #vh &= b == pattern[bs-1-y][bs-1-x]
            vh = False

            r090 &= b == pattern[x][y]
            r270 &= b == pattern[x][bs-1-y]
            r180 &= b == pattern[bs-1-x][bs-1-y]
            hmm &= b == pattern[bs-1-x][y]

    return o or h or v or vh or r090 or r270 or r180 or hmm

def enhance(block, rules):
    for pattern, enhanced in rules:
        if match(block, pattern):
            return valid(enhanced)
    raise ValueError("No match for block")

def block_size(grid, rules):
    if len(grid) % 2 == 0:
        return 2
    if len(grid) % 3 == 0:
        return 3
    raise ValueError("Weird grid")


def iterate(grid, rules):
    bs = block_size(grid, rules)
    s = len(grid) // bs
    print("{} -> {}".format(len(grid), (bs+1)*s))
    enhanced = (enhance(block, rules) for block in chunk(grid, bs))
    return stitch(enhanced, s)


def parse_rules(raw):
    import re
    for r in raw:
        m = re.match("(.*) => (.*)", r)
        a, b = m.groups()
        yield valid(a.split('/')), valid(b.split('/'))

def main():
    with open('input/21') as f:
        raw_rules = f.readlines()

    rules = list(parse_rules(raw_rules))
    grid = PATTERN.splitlines()

    for _ in range(18):
        grid = iterate(grid, rules)
        print(fmt(grid))
        print("")

    s = 0
    for line in grid:
        s += sum(1 for c in line if c == '#')

    print(s)

main()
