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
