import sys
from fractions import gcd
from itertools import combinations


def parse(f):
    _ = int(f.readline())
    buss_list = f.readline()
    busses = [(index, int(buss)) for (index, buss) in enumerate(buss_list.split(',')) if buss != 'x']
    return busses


def check_coprime(iterable):
    for a, b in combinations(iterable, 2):
        assert gcd(a, b) == 1


def prod(iterable):
    r = 1
    for i in iterable:
        r *= i
    return r


# Iterative Algorithm (xgcd)
def xgcd(a, b):
    x, y = 0, 1
    u, v = 1, 0
    while a != 0:
        q, r = b // a , b % a
        m, n = x -u * q, y - v * q
        b,a, x,y, u,v = a,r, u,v, m,n
    return b, x, y


def modinv(a, m):
    g, x, y = xgcd(a, m) 
    if g != 1:
        return None
    return x % m


def solve_crt(equations):
    m = [mi for _, mi in equations]
    check_coprime(m)
    M = prod(m)
    return sum(
        ai * (M // mi) * modinv(M // mi, mi) for ai, mi in equations
    ) % M


busses = parse(sys.stdin)
equations = [(bus - index, bus) for index, bus in busses]
t = solve_crt(equations)
print(t)
