import re

def load():
    with open('input/7') as f:
        for line in f:
            pattern = 'Step ([A-Z]) must be finished before step ([A-Z]) can begin.'
            m = re.match(pattern, line)
            yield m.groups()            

            
def can_assemble(unassembled, order, x):
    for a, b in order:
        if x == b and a in unassembled:
            return False
    return True

order = list(load())
everything = set([a for a, _ in order] + [b for _, b in order])
print(everything)
unassembled = set(everything)
assembled = []
while unassembled:
    available = []
    for x in unassembled:
        if can_assemble(unassembled, order, x):
            available.append(x)
    
    part = sorted(available)[0]
    unassembled.remove(part)
    assembled.append(part)

print(''.join(assembled))
