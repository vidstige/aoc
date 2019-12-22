from typing import List
import re

Deck = List[int]

def factory(n) -> Deck:
    return list(range(n))

def restack(deck: Deck) -> Deck:
    return deck[::-1]

def cut(deck: Deck, n: int) -> Deck:
    return deck[n:] + deck[:n]

def deal(deck: Deck, n: int) -> Deck:
    result = list(deck)
    for i, card in enumerate(deck):
        result[(i * n) % len(deck)] = card
    return result

def process(data: str, n=10007):
    deck = factory(n)
    instructions = [
        (r'deal with increment ([-\d]+)', deal),
        (r'deal into new stack', restack),
        (r'cut ([-\d]+)', cut)
    ]
    for line in data.splitlines():
        for pattern, f in instructions:
            m = re.match(pattern, line)
            if m:
                args = map(int, m.groups())
                deck = f(deck, *args)
    return deck

def load():
    with open('input/22') as f:
        return f.read()

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
print(process(load(), n=10007).index(2019))
