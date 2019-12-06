from collections import defaultdict

ex1 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""

ex2 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""

def load():
    with open('input/6') as f:
        return f.read()

def parse(data):
    orbits = defaultdict(list)
    for line in data.splitlines():
        a, b = line.split(')')
        orbits[a].append(b)
    return orbits

def search(orbits, name, d):
    if name not in orbits:
        return d
    names = orbits[name]
    return sum(search(orbits, n, d + 1) for n in names) + d


def edges(data):
    return [frozenset(line.split(')')) for line in data.splitlines()]


def distance(edges, start, stop):
    q = [(start, 0)]
    visited = set()
    while q:
        node, d = q.pop(0)
        if node == stop:
            return d - 2
        visited.add(node)
        for edge in edges:
            if node in edge:
                q.extend((n, d + 1) for n in edge - frozenset(node) - visited)
    
    return None



#print(search(parse(load()), 'COM', 0))
print(distance(edges(load()), 'YOU', 'SAN'))
