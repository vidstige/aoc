from collections import defaultdict

with open('input/2') as f:
    puzzle = f.readlines()

twos = 0
threes = 0
for line in puzzle:
    counter = defaultdict(int)
    for char in line:
        counter[char] += 1
    if any(c == 2 for c in counter.values()):
        twos += 1
    if any(c == 3 for c in counter.values()):
        threes += 1

print(twos * threes)

def part2(puzzle):
    for i, l1 in enumerate(puzzle):
        for l2 in puzzle[i+1:]:
            s = 0
            for c1, c2 in zip(l1, l2):
                if c1 != c2:
                    s += 1
            if s == 1:
                print(l1)
                print(l2)

part2(puzzle)

