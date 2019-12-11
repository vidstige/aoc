from intvm import load, Intcode
import subprocess

DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]


def bounding_box(grid):
    xmin = min(x for x, _ in grid)
    xmax = max(x for x, _ in grid)
    ymin = min(y for _, y in grid)
    ymax = max(y for _, y in grid)
    return xmin, xmax + 1, ymin, ymax + 1

def render(grid):
    xmin, xmax, ymin, ymax = bounding_box(grid)
    w, h = xmax - xmin, ymax - ymin
    im = bytearray(w * h)
    for (x, y), color in grid.items():
        x, y = x + xmin, y + ymin
        index = x + y * w
        im[index] = color * 255
    with open('11.raw', 'wb') as f:
        f.write(im)
    cmd = 'convert -size {w}x{h} -depth 8 gray:11.raw image.png'.format(w=w, h=h)
    subprocess.check_call(cmd.split())

def robot():
    vm = Intcode(load(11))
    grid = dict()
    di = 0
    p = (0, 0)

    grid[p] = 1
    while not vm.is_terminated():
        camera = grid.get(p, 0)
        vm.write(camera)
        color = vm.run()
        turn_right = vm.run()
        if color is not None:
            grid[p] = color        
        di = (di + (1 if turn_right == 1 else -1)) % len(DIRECTIONS)
        dx, dy = DIRECTIONS[di]
        x, y = p
        p = x + dx, y + dy

    print(len(grid))
    render(grid)

robot()
