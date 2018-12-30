import heapq
from functools import lru_cache
from tqdm import tqdm

@lru_cache(maxsize=1024*1024)
def erosion(p, target, depth):
    return (index(p, target, depth) + depth) % 20183

@lru_cache(maxsize=1024*1024)
def index(p, target, depth):
    if p == (0, 0):
        return 0
    if p == target:
        return 0
    x, y = p
    if x == 0:
        return y * 48271
    if y == 0:
        return x * 16807
    return erosion((x-1, y), target, depth) * erosion((x, y-1), target, depth)

def risk(e):
    return e % 3

def evaluate(target, depth):
    tx, ty = target
    s = 0
    for y in range(ty + 1):
        for x in range(tx + 1):
            s += risk(erosion((x, y), target, depth))
    return s

def type_at(p, target, depth):
    if p == target:
        return 0
    if p == (0, 0):
        return 0
    return erosion(p, target, depth) % 3

def neighbours(x, y):
    yield x + 1, y
    yield x, y + 1
    yield x - 1, y
    yield x, y - 1

ROCKY = 0
WET = 1
NARROW = 2

NEITHER = 0
TORCH = 1
CLIMBING_GEAR = 2

def fastest(target, depth):
    # from type, tool => minutes, tool
    options = {
        ROCKY: (TORCH, CLIMBING_GEAR),
        WET: (NEITHER, CLIMBING_GEAR),
        NARROW: (NEITHER, TORCH)
    }
    
    # Tuples of: minutes, x, y, tool
    heap = []
    heapq.heappush(heap, (1, 0, 0, TORCH))
    visited = {}
    while heap:
        m, x, y, tool = heapq.heappop(heap)
        p = x, y
        if p not in visited or visited[p] > m:
            for n in neighbours(x, y):
                nx, ny = n
                if nx < 0 or ny < 0:
                    continue
                for option in options[type_at(n, target, depth)]:
                    dm = 1 if tool == option else 7
                    heapq.heappush(heap, (m + dm, nx, ny, option))
        if p == target:
            return m
        visited[p] = m
    
def main():
    #depth: 11109
    #target: 9,731

    #print(evaluate(target=(10, 10), depth=510))
    #print(evaluate(target=(9,731), depth=11109))

    
    print(fastest(target=(10, 10), depth=510))
    print(fastest(target=(9,731), depth=11109))

main()
