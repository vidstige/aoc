from itertools import cycle
import math
import re
import sys
from typing import Dict, Iterable, Sequence, TextIO, Tuple

def parse(f: TextIO):
    lookup = {'L': 0, 'R': 1}
    raw_instructions = f.readline().rstrip()
    instructions = [lookup[i] for i in raw_instructions]
    network = {}
    for line in f:
        match = re.match(r'([0-9A-Z]+) = \(([0-9A-Z]+), ([0-9A-Z]+)\)', line)
        if match:
            node, left, right = match.group(1), match.group(2), match.group(3)
            network[node] = (left, right)

    return instructions, network


def steps(start: str, stops: Tuple[str], instructions, network) -> int:
    node = start
    n = 0
    # infinite loop
    for instruction in cycle(instructions):
        if node in stops:
            return n
            #print(n)
        node = network[node][instruction]
        n += 1
    return n


instructions, network = parse(sys.stdin)
# first star
#print(steps("AAA", ("ZZZ",), instructions, network))


def prime_factors(n: int) -> Iterable[int]:
    i = 2
    while i * i <= n:
        if n % i == 0:
            n //= i
            yield i            
        else:
            i += 1
    if n > 1:
        yield n


def ghost(instructions: Sequence[int], network: Dict[str, Tuple[str, str]]):
    nodes = [node for node in network.keys() if node.endswith('A')]
    stops = [node for node in network.keys() if node.endswith('Z')]
    factors = set()
    for node in nodes:
        s = steps(node, stops, instructions, network)
        factors |= set(prime_factors(s))
    return math.prod(factors)

print(ghost(instructions, network))
