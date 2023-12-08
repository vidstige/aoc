from itertools import cycle
import re
import sys
from typing import TextIO

def parse(f: TextIO):
    lookup = {'L': 0, 'R': 1}
    raw_instructions = f.readline().rstrip()
    instructions = [lookup[i] for i in raw_instructions]
    f.readline()  # skip empty line
    network = {}
    for line in f:
        match = re.match(r'([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)', line)
        if match:
            node, left, right = match.group(1), match.group(2), match.group(3)
            network[node] = (left, right)

    return instructions, network


def steps(start: str, stop: str, instructions, network) -> int:
    node = start
    n = 0
    # infinite loop
    for instruction in cycle(instructions):
        print(node)
        if node == stop:
            return n
        node = network[node][instruction]
        n += 1


instructions, network = parse(sys.stdin)
print(steps("AAA", "ZZZ", instructions, network))