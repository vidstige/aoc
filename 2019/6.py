from collections import defaultdict

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

data = """COM)B
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

print(search(parse(load()), 'COM', 0))