import re

def load():
    with open('input/7') as f:
        for line in f:
            pattern = 'Step ([A-Z]) must be finished before step ([A-Z]) can begin.'
            m = re.match(pattern, line)
            yield m.groups()            

            
def can_assemble(assembled, order, p):
    for a, b in order:
        if p == b and a not in assembled:
            return False
    return True


def duration(part):
    return ord(part) - 4


order = list(load())
everything = set([a for a, _ in order] + [b for _, b in order])
unassembled = set(everything)
assembled = []
n = 5
t = 0
left = [0] * n
work = [None] * n
while len(assembled) < len(everything):
    for i in range(len(left)):
        if left[i] == 0 and work[i]:
            # finish part
            assembled.append(work[i])
            work[i] = None
        left[i] -= 1

    available = list(sorted([p for p in unassembled if can_assemble(assembled, order, p)]))
#    if not available and not all(work):
#        raise Exception('No part available')

    while None in work and available:
        part = available.pop(0)
        unassembled.remove(part)
        index = work.index(None)
        work[index] = part
        left[index] = duration(part) - 1

    print(t, '\t', '\t'.join(w or ' ' for w in work), ''.join(assembled))
    t += 1

print(''.join(assembled))
print('{}s'.format(t))
