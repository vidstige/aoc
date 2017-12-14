from day10 import elf_hash as knot_hash
ex = "flqrgnkx"
data = "oundnydw"

def defrag(disk):
    return len(disk)

def create_disk(data):
    tmp = set()
    for y in range(128):
        hash_str = knot_hash('{}-{}'.format(data, y))
        h  = int(hash_str, 16)
        row = "{:0128b}".format(h)
        for x, c in enumerate(row):
            if c == '1':
                tmp.add((x, y))
    return tmp

DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
def regions(disk):
    n = 0
    while disk:
        # 1. Find a used square
        stack = [disk.pop()]
        n += 1

        # 2. Search neighbours
        while stack:
            x, y = stack.pop()
            for dx, dy in DIRECTIONS:
                p = (x + dx, y + dy) 
                if p in disk:
                    stack.append(p)
                    disk.remove(p)

    return n
    

#disk = create_disk(ex)
#print(disk)
#print(defrag(disk))

disk = create_disk(data)
print(regions(disk))
