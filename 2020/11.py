import sys

def parse(f):
    layout = {}
    for y, line in enumerate(f):
        for x, c in enumerate(line.strip()):
            layout[(x, y)] = c
    return layout

NEIGHBOURS = [
    (-1, -1),
    ( 0, -1),
    ( 1, -1),
    (-1,  0),
    ( 1,  0),
    (-1,  1),
    ( 0,  1),
    ( 1,  1),
]

def find_neighbours(key, layout):
    x, y = key
    return [layout[(x+dx, y + dy)] for dx, dy in NEIGHBOURS if (x + dx, y + dy) in layout]

def step_cell(value, neighbours):
    if value == 'L' and '#' not in neighbours:
        return '#'
    if value == '#' and len([n for n in neighbours if n == '#']) >= 4:
        return 'L'
    return value

def step(layout):
    return {key: step_cell(value, find_neighbours(key, layout)) for key, value in layout.items()}

def print_layout(layout):
    x0, y0 = min(layout)
    x1, y1 = max(layout)
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            print(layout.get((x, y), 'x'), end='')
        print()


layout = parse(sys.stdin)
while True:
    #print_layout(layout)
    next_layout = step(layout)
    if next_layout == layout:
        break
    layout = next_layout

print(len([value for value in layout.values() if value == '#']))