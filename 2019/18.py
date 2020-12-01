ex1="""#########
#b.A.@.a#
#########"""
ex2="""########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""
ex3="""########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""
ex4="""#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""
ex5="""########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""

KEYS = set('abcdefghijklmnopqrstuvwxyz')
DOORS = set('abcdefghijklmnopqrstuvwxyz'.upper())

def neighbours(position):
    x, y = position
    yield x + 1, y
    yield x, y + 1
    yield x - 1, y
    yield x, y - 1

def parse(data):
    grid = {}
    position = None
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == '@':
                c = '.'
                position = x, y
            grid[(x, y)] = c
    return grid, position

def is_key(grid, position):
    return grid[position] in KEYS

def pick_up(keys, grid, position):
    """Picks up key at position, if any"""
    if is_key(grid, position):
        return frozenset(keys.union({grid[position]}))
    return keys

def can_go(grid, position, keys):
    if grid[position] == '.' or grid[position] in KEYS:
        return True
    return grid[position].lower() in keys

# seach(KEYS)
# search(keys) = best(search(keys - key) + cost(key), search(b + keys - b, etc)
from collections import defaultdict
def build(grid, position):
    """Computes a graph connecting all the keys"""
    edges = defaultdict(list)
    all_keys = set((p, v) for p, v in grid.items() if v in KEYS)
    all_keys.add((position, '@'))
    while all_keys:
        # find steps between start and all other keys
        start_position, start_key = all_keys.pop()
        queue = [(start_position, 0, frozenset())]
        visited = set()
        while queue:
            p, steps, required = queue.pop(0)
            visited.add(p)
            if grid[p] in KEYS and grid[p] != start_key:
                #edge = frozenset((start_key, grid[p])), steps, required
                edges[start_key].append((steps, grid[p], required))
            if grid[p] in DOORS:
                # add the required key for he door
                required = required.union(frozenset(grid[p].lower()))
            for n in neighbours(p):
                if n not in visited and grid[n] != '#':
                    queue.append((n, steps + 1, required))
    return edges

def other(pair, a):
    singleton = pair.difference(frozenset(a))
    assert len(singleton) == 1
    return next(iter(singleton))

def get_state(carried):
    #return carried[-1], frozenset(carried[:-1])
    return carried

def solve(grid, position):
    goal = set(k for k in grid.values() if k in KEYS)
    edges = build(grid, position)
    queue = [(0, '@')]
    visited = set()
    result = []
    while queue:
        steps, carried = queue.pop(0)
        print(carried)
        state = get_state(carried)
        if state in visited:
            continue
        visited.add(state)

        if frozenset(carried) >= goal:
            #print(carried, steps)
            result.append(steps)
            return steps

        queue.sort()
        key = carried[-1]
        for s, o, required in sorted(edges[key], reverse=True):
            if required <= frozenset(carried) and o not in carried:
                queue.append((steps + s, carried + o))

    return min(result)

def load():
    with open('input/18') as f:
        return f.read()

print(solve(*parse(ex1)), 8)
print(solve(*parse(ex2)), 86)
print(solve(*parse(ex3)), 132)
print(solve(*parse(ex4)), 136)
print(solve(*parse(ex5)), 81)
#print(solve(*parse(load())), 81)
