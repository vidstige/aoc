import re
from tqdm import tqdm

def load(filename):
    with open(filename) as f:
        for line in f:
            match = re.match(r'x=(\d+), y=(\d+).\.(\d+)', line)
            if match:
                x, y0, y1 = [int(i) for i in match.groups()]
                for y in range(y0, y1 + 1):
                    yield x, y
            match = re.match(r'y=(\d+), x=(\d+).\.(\d+)', line)
            if match:
                y, x0, x1 = [int(i) for i in match.groups()]
                for x in range(x0, x1 + 1):
                    yield x, y


def step(clay, still, flowing):
    blocked = clay | still
    new_flowing = set()
    for x, y in flowing:
        if (x, y + 1) in blocked:
            if (x - 1, y) not in blocked:
                new_flowing.add((x - 1, y))
            if (x + 1, y) not in blocked:
                new_flowing.add((x + 1, y))

        else:
            new_flowing.add((x, y + 1))

    flowing |= new_flowing

    stillify = set()
    # Check for still water
    for x, y in flowing:
        xl = x
        while (xl, y) in flowing and (xl, y + 1) not in blocked:
            xl -= 1
        xr = x
        while (xr, y) in flowing and (xl, y + 1) not in blocked:
            xr += 1
        if (xl, y) in clay and (xr, y) in clay:
            for xx in range(xl + 1, xr):
                stillify.add((xx, y))
    
    still |= stillify
    flowing -= stillify
    return bool(new_flowing) or bool(stillify)


def bounding(clay):
    xmin = min(x for x, _ in clay)
    xmax = max(x for x, _ in clay)

    ymin = min(y for _, y in clay)
    ymax = max(y for _, y in clay)
    return xmin, xmax + 1, ymin, ymax + 1

def inside(b, w):
    _, y = w
    _, _, ymin, ymax = b
    return y >= ymin and y < ymax

def draw(clay, still, flowing):
    xmin, xmax, ymin, ymax = bounding(clay)
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            p = x, y
            if p in clay:
                print('#', end='')
            elif p in still:
                print('~', end='')
            elif p in flowing:
                print('|', end='')
            else:
                print(' ', end='')
        print()
            

def main(clay):
    flowing = {(500, 0)}
    still = set()
    b = bounding(clay)
    progress = tqdm()
    while step(clay, still, flowing):
        progress.update(1)
        #draw(clay, still, flowing)
        #input()
        pass
    
    draw(clay, still, flowing)
    print(len([w for w in still | flowing if inside(b, w)]))

clay = set(load('input/17'))
main(clay)
