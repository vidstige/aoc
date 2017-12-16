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
    
    return [initial.index(x) for x in d]

ex = """s1,x3/4,pe/b"""
n = 5
initial = list(alphabet[0:n])
m = dance(ex, initial)
d = initial
print("".join(d))
d = [d[x] for x in m]  # fast program 
print("".join(d))
d = [d[x] for x in m]  # fast program 
print("".join(d))


#n = 16
#with open('input/16') as f:
#    program = f.read()

#initial = list(alphabet[0:n])
#m = dance(program, d)


#d = initial.copy()
#for _ in tqdm(range(1000000000), mininterval=0.5):
#    d = [d[x] for x in m]  # fast program 

#print(''.join(d))
