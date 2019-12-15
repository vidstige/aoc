from intvm import Intcode, load

DX = {'E': 1, 'W': -1, 'N': 0, 'S': 0}
DY = {'E': 0, 'W': 0, 'N': -1, 'S': 1}
CMD = {'N': 1, 'S': 2, 'W': 3, 'E': 4}


def bounding_box(grid):
    xmin = min(x for x, _ in grid)
    xmax = max(x for x, _ in grid)
    ymin = min(y for _, y in grid)
    ymax = max(y for _, y in grid)
    return xmin, xmax + 1, ymin, ymax + 1

def draw(grid, bounds=None, X=None):
    if not grid:
        return
    xmin, xmax, ymin, ymax = bounds or bounding_box(grid)
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            if (x, y) == X:
                character = 'X'
            else:
                character = grid.get((x, y), ' ')
            print(character, end='')
        print()


def coordinate(sequence):
    return sum(DX[d] for d in sequence), sum(DY[d] for d in sequence)

def search(program):
    stack = [('', program)]
    grid = dict()
    oxygen = None
    while stack:
        sequence, p = stack.pop(0)
        c = coordinate(sequence)
        #draw(grid, X=c)

        # Update map
        grid[c] = '.'

        # Run sequence
        for d in 'NSWE':
            ds = sequence + d
            dc = coordinate(ds)

            if dc in grid:
                continue

            vm = Intcode(p)
            vm.write(CMD[d])
            status = vm.run()
        
            if status == 0:
                grid[dc] = '#'
            elif status == 1:
                # Take new step
                stack.append((ds, vm.program))
            elif status == 2:
                oxygen = ds
                stack.append((ds, vm.program))
            else:
                print("bad status:", status)
    return grid, oxygen

def oxygnize(grid, oxygen):
    t = 0
    grid[coordinate(oxygen)] = 'O'
    
    while any(v == '.' for v in grid.values()):
        draw(grid)
        # find all coordinates with oxygen
        o = [key for key, value in grid.items() if value == 'O']
        # spread
        for c in o:
            x, y = c
            for d in 'NSWE':
                cc = x + DX[d], y + DY[d]
                if grid[cc] == '.':
                    grid[cc] = 'O'
        t += 1
    print(t)


grid, oxygen = search(load(day=15))
print("distance to oxygen:", len(oxygen))
draw(grid, X=coordinate(oxygen))
oxygnize(grid, oxygen)