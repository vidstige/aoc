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
    stack = ['']
    grid = dict()
    while stack:
        sequence = stack.pop(0)
        c = coordinate(sequence)
        #draw(grid, X=c)
        # Run sequence
        vm = Intcode(program)
        status = None
        for d in sequence:
            vm.write(CMD[d])
            status = vm.run()
        
        if status == 0:
            #assert c not in grid
            grid[c] = '#'
        elif status == 1 or status is None:
            #assert c not in grid
            # Update map
            grid[c] = '.'

            # Take new step
            for d in 'NSWE':
                ds = sequence + d
                if coordinate(ds) not in grid:
                    stack.append(ds)
        elif status == 2:
            print("gold", len(sequence))
            return "gold"
        else:
            print("bad status:", status)

search(load(day=15))
