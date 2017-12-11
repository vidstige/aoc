import operator

ex = [3, 4, 1, 5]
data = '63,144,180,149,1,255,167,84,125,65,188,0,2,254,229,24'

def format(l, p):
    return ' '.join("[{}]".format(x) if i == p else str(x) for i, x in enumerate(l))

def sublist(l, start, length):
    return [l[i % len(l)] for i in range(start, start + length)]

def insert(l, start, new):
    for i, v in enumerate(new):
        l[(start + i) % len(l)] = v

def knot(lengths, n=256, rounds=1):
    l = list(range(n))
    p = 0
    skip = 0
    for _ in range(rounds):
        for length in lengths:
            new = list(reversed(sublist(l, p, length)))
            insert(l, p, new)
            
            p = (p + length + skip) % n
            skip += 1

    return l


def dense(sparse):
    d = []
    for i in range(16):
        acc = 0
        for j in range(i*16, i*16+16):
            acc ^= sparse[j]
        d.append(acc)
    return d


def elf_hash(data):
    suffix = [17, 31, 73, 47, 23]
    lengths = [ord(c) for c in data]
    sparse = knot(lengths + suffix, rounds=64)
    return ''.join('%02x'%i for i in dense(sparse))

#after = knot(ex, 5)
#print(after)
#print(after[0] * after[1])

#after = knot(data, 256)
#print(after)
#print(after[0] * after[1])

## part 2
ex = {
    '': 'a2582a3a0e66e6e86e3812dcb672a272',
    'AoC 2017': '33efeb34ea91902bb2f59c9920caa6cd',
    '1,2,3': '3efbe78a8d82f29979031a4aa0b16a9d',
    '1,2,4': '63960835bcdc130f0b66d7ff4f6a5a8e'
}


for input, expected in ex.items():
    actual = elf_hash(input)

    if actual == expected:
        print("ok")
    else:
        print("hash({}) should be {}, but was {}".format(input, expected, actual))

print(data)
print(elf_hash(data))