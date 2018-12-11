def hundreds(x):
    return int(str(x // 100)[-1])
    
def cell(serial, p):
    x, y = p
    rack_id = x + 10
    level = (rack_id * y + serial) * rack_id
    return hundreds(level) - 5

def grid(w, h):
    for y in range(w):
        for x in range(h):
            yield x, y

def power_levels(serial, size=300, kernel=3):
    levels = {}
    kernel = 3
    for x, y in grid(size - kernel, size - kernel):
        p = x + 1, y + 1
        levels[p] = sum(cell(serial, (x + a + 1, y + b + 1)) for a, b in grid(3, 3))
    return levels

def highest(levels):
    return max((l, c) for c, l in levels.items())

#print(cell(71, (101,153)))
#print(18, highest(power_levels(18)))
#print(42, highest(power_levels(42)))
print(1955, highest(power_levels(1955)))


    

