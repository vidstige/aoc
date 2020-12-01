from itertools import islice, chain
from typing import Iterable, Iterator
import re


def aslist(deck):
    return [deck.get(i) for i in range(len(deck))]


class ReversedDeck:
    def __init__(self, inner):
        self.inner = inner

    def __len__(self):
        return self.inner.__len__()
    
    def get(self, index):
        assert index >= 0
        return self.inner.get(self.inner.__len__() - 1 - index)


class CutDeck:
    def __init__(self, inner, n):
        self.inner = inner
        self.n = n

    def __len__(self):
        return self.inner.__len__()
    
    def get(self, index):
        assert index >= 0
        l = self.inner.__len__()
        if self.n >= 0:
            return self.inner.get((index + self.n) % l)
        return self.inner.get((l + index + self.n) % l)


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


class DealedDeck:
    def __init__(self, inner, n):
        self.inner = inner
        self.n = n
        self.m = modinv(self.n, len(self))

    def __len__(self):
        return self.inner.__len__()

    def get(self, index):
        assert index >= 0
        i = (index * self.m) % len(self)
        return self.inner.get(i)


class FactoryDeck:
    def __init__(self, n: int):
        self.n = n

    def __len__(self):
        return self.n

    def get(self, index):
        return index


def match_line(line):
    instructions = [
        (r'deal with increment ([-\d]+)', DealedDeck),
        (r'deal into new stack', ReversedDeck),
        (r'cut ([-\d]+)', CutDeck)
    ]
    for pattern, f in instructions:
        m = re.match(pattern, line)
        if m:
            args = map(int, m.groups())
            return f, args
    raise Exception('Unknown line:' + line)

def process(deck, data: str):
    for line in data.splitlines():
        f, args = match_line(line)
        #print(aslist(deck))
        deck = f(deck, *args)

    return deck


def load():
    with open('input/22') as f:
        return f.read()

def verify(data, expected):
    deck = FactoryDeck(10)
    actual = ' '.join(map(str, aslist(process(deck, data))))
    if actual == expected:
        print('ok')
    else:
        print('{} != {}'.format(actual, expected))

ex1="""deal with increment 7
deal into new stack
deal into new stack"""
ex2="""cut 6
deal with increment 7
deal into new stack"""
ex3="""deal with increment 7
deal with increment 9
cut -2"""
ex4="""deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""
verify(ex1, '0 3 6 9 2 5 8 1 4 7')
verify(ex2, '3 0 7 4 1 8 5 2 9 6')
verify(ex3, '6 3 0 7 4 1 8 5 2 9')
verify(ex4, '9 2 5 8 1 4 7 0 3 6')

history = []
deck = FactoryDeck(n=10007)
i = 0
while True:
    print(i)
    tmp = aslist(process(deck, load()))
    if tmp in history:
        print(i)
    history.append(tmp)
    i += 1
    
