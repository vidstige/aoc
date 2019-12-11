from intvm import load, Intcode

DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]

def robot():
    vm = Intcode(load(11))
    grid = dict()
    di = 0
    p = (0, 0)

    while not vm.is_terminated():
        camera = grid.get(p, 0)
        vm.write(camera)
        color = vm.run()
        turn_right = vm.run()
        grid[p] = color        
        di = (di + (1 if turn_right == 1 else -1)) % len(DIRECTIONS)
        dx, dy = DIRECTIONS[di]
        x, y = p
        p = x + dx, y + dy

    print(len(grid))

robot()
