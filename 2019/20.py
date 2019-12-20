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
ex3="""             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """

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

def get_bounds(grid):
    xmin = min(x for x, _ in grid)
    xmax = max(x for x, _ in grid)
    ymin = min(y for _, y in grid)
    ymax = max(y for _, y in grid)
    return xmin, xmax, ymin, ymax

def is_outside(p, bounds):
    x, y = p
    xmin, xmax, ymin, ymax = bounds
    return x == xmin + 2 or x == xmax - 2 or y == ymin + 2 or y == ymax - 2

DELTAS = {
    (True, False): -1,
    (False, True): 1,
}

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
    bounds = get_bounds(grid)
    # add portal edges
    for portal, sides in portals.items():
        if len(sides) == 2:
            blue, red = sides
            b = single(n for n in neighbours_many(*blue) if grid.get(n) == '.')
            r = single(n for n in neighbours_many(*red) if grid.get(n) == '.')

            tmp = is_outside(b, bounds), is_outside(r, bounds)
            if tmp not in DELTAS:
                print(portal)
            delta = DELTAS[tmp]
    
            edges[b].add((r, delta))
            edges[r].add((b, -delta))
        else:
            assert len(sides) == 1, "{}: {}".format(portal, len(sides))

    # add grid edges
    for p, v in grid.items():
        if v == '.':
            for n in neighbours(p):
                if grid.get(n) == '.':
                    edges[p].add((n, 0))
                    edges[n].add((p, 0))

    return edges, start, end

def search(edges, start, end):
    def by_level(node):
        return node[1]

    queue = [(start, 0, 0)]
    visited = set()
    while queue:
        lvls = [q[1] for q in queue]
        #print(lvls)

        p, level, steps = queue.pop(0)
        if (p, level) in visited:
            continue
        visited.add((p, level))        
        #print(p, level)
        if p == end and level == 0:
            return steps
        queue.sort(key=by_level)
        for n, level_delta in edges[p]:
            #if (n, level) not in visited:
            # can't go out of outermost level
            if level + level_delta >= 0:
                queue.append((n, level + level_delta, steps + 1))

    return None

def solve(data, expected):
    actual = search(*parse(data))
    print(actual, expected, '✔' if actual == expected else 'x')    

def load():
    with open('input/20') as f:
        return f.read()
    
#solve(ex1, 26)
#solve(ex2, 58)
solve(ex3, 396)
solve(load(), None)
