ex = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""

def parse(data):
    lines = [line.split('/') for line in data.splitlines()]
    return set((int(a), int(b)) for a, b in lines)

def search(initial_parts, first):
    stack = [(set(initial_parts), first, [])]
    while stack:
        parts, n, route = stack.pop()

        # yield everything
        yield route

        # find all parts that fit and push
        potential = set(parts)
        rest = set()
        before = len(stack)
        while potential:
            a, b = potential.pop()
            if a == n:
                stack.append((potential | rest, b, route + [(a, b)]))
            if b == n:
                stack.append((potential | rest, a, route + [(b, a)]))
            rest.add((a, b))


def bridge(parts):
    lengths = []
    for route in search(parts, 0):
        length = len(route)
        strength = sum(a + b for a, b in route)
        lengths.append((length, strength))
    print(max(lengths))

bridge(parse(ex))

with open('input/24') as f:
    bridge(parse(f.read()))
