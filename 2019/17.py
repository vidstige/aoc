from intvm import Intcode, load
import sys

def neighbours(x, y):
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1

def intersections(grid):
    for x, y in grid:
        if all(n in grid for n in neighbours(x, y)):
            yield x, y

def alignment(grid):
    return sum(x * y for x, y in intersections(grid))

program = load(day=17)
vm = Intcode(program)

grid = set()
x, y = 0, 0
while not vm.is_terminated():
    c = vm.run()
    if c == 10:
        x, y = 0, y + 1
    if c == 35:
        grid.add((x, y))
    if c in (35, 46):
        x += 1

print(alignment(grid))
