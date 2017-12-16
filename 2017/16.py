from string import ascii_lowercase as alphabet
from tqdm import tqdm

def rotate(l, n):
    return l[n:] + l[:n]

def dance(program, initial):
    d = initial.copy()
    for line in program.split(','):
        rest = line[1:]
        if line[0] == 's':
            #print('spin {}'.format(int(rest)))
            d = rotate(d, -int(rest))
        if line[0] == 'x':
            a, b = rest.split('/')
            a, b = int(a), int(b)
            d[a], d[b] = d[b], d[a]
        if line[0] == 'p':
            pa, pb = rest.split('/')
            a, b = d.index(pa), d.index(pb)
            d[a], d[b] = d[b], d[a]
    
    return d

def find_loop(program, initial):
    d = initial.copy()
    for i in range(1000000000):
        d = dance(program, d)
        if d == initial:
            return i + 1
    return None


ex = """s1,x3/4,pe/b"""
n = 5
initial = list(alphabet[0:n])
d = initial
d = dance(ex, d)
print("".join(d))
d = dance(ex, d)
print("".join(d))

n = 16
with open('input/16') as f:
    program = f.read()

initial = list(alphabet[0:n])
cycle = find_loop(program, initial)

d = initial
for _ in range(1000000000 % cycle):
    d = dance(program, d)
    
print(''.join(d))
