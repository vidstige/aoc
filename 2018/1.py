with open('input/1') as f:
    puzzle_input = f.readlines()

from itertools import cycle

frequencies = [int(l) for l in puzzle_input]
f = 0
history = set()
for df in cycle(frequencies):
    if f in history:
        break
    history.add(f)
    f += df

#print(history)
print(f)