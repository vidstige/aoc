ex = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""

def parse(data):
    nodes = set()
    edges = {}
    for line in data.splitlines():
        n1, targets = line.split('<->')
        n1 = n1.strip()
        nodes.add(n1)
        for ns in targets.split(','):
            n2 = ns.strip()
            nodes.add(n2)
            edges.setdefault(n1, set()).add(n2)
            edges.setdefault(n2, set()).add(n1)

    return nodes, edges


def partition(nodes, edges):
    unvisited = set(nodes)
    groups = []
    while unvisited:
        todo = [next(iter(unvisited))]

        # visit group
        g = []
        while todo:
            node = todo.pop()
            if node in unvisited:
                g.append(node)
                unvisited.remove(node)
                for n in edges[node]:
                    todo.append(n)

        groups.append(g)
    
    return groups


def run(data):
    nodes, edges = parse(data)
    g = partition(nodes, edges)
    print(len(g))

run(ex)
with open('input/12') as f:
    run(f.read())

