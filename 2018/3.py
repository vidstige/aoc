import re

def load():
    with open('input/3') as f:
        for line in f.readlines():
            match = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
            if match:
                yield tuple(int(x) for x in match.groups())

def overlap(r1, r2):
    _, x1, y1, w1, h1 = r1
    _, x2, y2, w2, h2 = r2
    
    xx1, xx2 = max(x1, x2), min(x1 + w1, x2 + w2)
    yy1, yy2 = max(y1, y2), min(y1 + h1, y2 + h2)
    if xx1 < xx2 and yy1 < yy2:
        return range(xx1, xx2), range(yy1, yy2)
    return None

def mark(sheet, xyr):
    if not xyr:
        return
    xr, yr = xyr
    for y in yr:
        for x in xr:
            sheet[(x, y)] = 1


def main():
    rectangles = list(load())
    sheet = {}

    for i, r1 in enumerate(rectangles):
        for r2 in rectangles[i + 1:]:
            mark(sheet, overlap(r1, r2))


    print(sum(sheet.values()))

main()
