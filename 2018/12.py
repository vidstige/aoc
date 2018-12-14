
def load(filename):
    with open(filename) as f:
        initial = f.readline()[len('initial state: '):].rstrip()
        f.readline()
        
        rules = []
        for line in f.readlines():
            left = line[:5]
            right = line.rstrip()[-1]
            rules.append((left, right))
    
        return initial, rules

def generation(state, rules):
    # zero pad
    index, state = state
    s = "...{}...".format(state)
    result = [c for c in s]
    #result = ['.' for _ in s]
    for i in range(2, len(s)-2):
        #print('  ', s[i-2:i+3])
        for pattern, produce in rules:
            if s[i-2:i+3] == pattern:
                result[i] = produce
    
    res = ''.join(result)
    return index + res.index('#') - 3, res.strip('.')


def pot_numbers(state):
    offset, s = state
    for i, c in enumerate(s):
        if c == '#':
            yield i + offset

from tqdm import tqdm

def main():
    initial, rules = load('input/12')
    state = 0, initial
    for g in range(300):
        ##print(g, state)
        state = generation(state, rules)
        print(g, sum(pot_numbers(state)))
    
    
#main()

after300 = 57521
diff = 194
gens = 50000000000 - 300
print(after300 + gens*diff)
