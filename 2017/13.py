import itertools

ex = """0: 3
1: 2
4: 4
6: 4"""

def parse(data):
    ranges = {}
    for line in data.splitlines():
        depth, range1 = line.split(': ')
        depth = int(depth)
        ranges[depth] = int(range1)
    return ranges


def severity(interceptions, ranges):
    s = 0
    for i in interceptions:
        s += i * ranges[i]
    return s

def step(t, ranges, scanners):
    for s in scanners:
        direction = 1 if (t // (ranges[s]-1)) % 2 == 0 else -1
        scanners[s] += direction

next_initial = None
def run(ranges, delay=0):
    global next_initial
    if delay == 0:
        # all scanners start at 0
        scanners = {d: 0 for d in ranges}        
    else:
        scanners = next_initial

    next_initial = scanners.copy()
    step(delay, ranges, next_initial)

    t = delay

    interceptions = []
    for d in range(max(ranges)+1):
        # 1. intercept
        if scanners.get(d) == 0:
            interceptions.append(d)

        # 2. step scanners
        step(t, ranges, scanners)
        t += 1

    return interceptions

def first_free(data):
    for delay in itertools.count():
        interceptions = run(data, delay=delay)
        if len(interceptions) == 0:
            return delay
        if delay % 13 == 0:
            print(' {}'.format(delay), end="\r")
    return None

data = parse(ex)
print(severity(run(data), data))
print(first_free(data))

with open('input/13') as f:
    data = parse(f.read())

print(severity(run(data), data))
print(first_free(data))
