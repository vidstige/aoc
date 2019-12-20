from collections import defaultdict

ex1="""         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """
ex2="""                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               """

def neighbours(p):
    x, y = p
    yield x - 1, y
    yield x, y - 1
    yield x + 1, y
    yield x, y + 1


def neighbours_many(*args):
    ns = set()
    for a in args:
        for n in neighbours(a):
            ns.add(n)
    return ns

def single(iterable):
    return next(iter(iterable))

def parse(data):
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, character in enumerate(line):
            if not character.isspace():
                grid[(x, y)] = character

    letters = {p: v for p, v in grid.items() if v not in ('#', '.')}
    portals = defaultdict(list)  
    while letters:
        p, letter = letters.popitem()
        for n in neighbours(p):
            if n in letters:
                other = letters.pop(n)
                portal = ''.join([letter, other])
                portals[portal].append((p, n))

    # find start & end points
    aa = single(portals['AA'])
    start = single(n for n in neighbours_many(*aa) if grid.get(n) == '.')
    zz = single(portals['ZZ'])
    end = single(n for n in neighbours_many(*zz) if grid.get(n) == '.')

    edges = defaultdict(set)
    # add portal edges
    for portal, sides in portals.items():
        if len(sides) == 2:
            blue, red = sides
            b = single(n for n in neighbours_many(*blue) if grid.get(n) == '.')
            r = single(n for n in neighbours_many(*red) if grid.get(n) == '.')
            edges[b].add(r)
            edges[r].add(b)
        else:
            assert len(sides) == 1, "{}: {}".format(portal, len(sides))

    # add grid edges
    for p, v in grid.items():
        if v == '.':
            for n in neighbours(p):
                if grid.get(n) == '.':
                    edges[p].add(n)
                    edges[n].add(p)

    return edges, start, end

def search(edges, start, end):
    queue = [(start, 0)]
    visited = set()
    while queue:
        p, steps = queue.pop(0)
        visited.add(p)
        if p == end:
            return steps
        for n in edges[p]:
            if n not in visited:
                queue.append((n, steps + 1))
    return None

def solve(data, expected):
    actual = search(*parse(data))
    print(actual, expected, '✔' if actual == expected else 'x')    

def load():
    with open('input/20') as f:
        return f.read()
    
solve(ex1, 23)
solve(ex2, 58)
solve(load(), None)
