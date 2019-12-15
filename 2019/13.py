from intvm import Intcode, load
from draw import draw

vm = Intcode(program=load(day=13))

grid = {}
while not vm.is_terminated():
    x = vm.run()
    y = vm.run()
    tile = vm.run()
    if x is not None and y is not None and tile is not None:
        grid[(x, y)] = tile

draw(grid)
print(len([t for t in grid.values() if t == 2]))