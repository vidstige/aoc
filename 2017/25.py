import re 

def parse(lines):
    n = (len(lines) - 3) // 10
    i = 0

    initial = re.match('Begin in state ([A-Z])\.', lines[0]).group(1)
    steps = int(re.search('(\d+)', lines[1]).group(1))

    rules = {}
    for i in range(n+1):
        i = 3 + i * 10
        state = re.match('In state ([A-Z]):', lines[i]).group(1)

        current = re.search('([01])', lines[i+1]).group(1)
        w = re.search('([01])', lines[i+2]).group(1)
        d = re.search('(left|right)', lines[i+3]).group(1)
        s = re.search('state ([A-Z])', lines[i+4]).group(1)
        rules[(state, current)] = (w, d, s)

        current = re.search('([01])', lines[i+5]).group(1)
        w = re.search('([01])', lines[i+6]).group(1)
        d = re.search('(left|right)', lines[i+7]).group(1)
        s = re.search('state ([A-Z])', lines[i+8]).group(1)
        rules[(state, current)] = (w, d, s)

    return rules, initial, steps

def turing(rules, initial, n):
    ones = set()
    cursor = 0
    state = initial
    next_state = None

    for i in range(n):
        if i % 10001 == 0:
            print("\r{}".format(100*i // n), end='')

        c = '1' if cursor in ones else '0'
        w, d, s = rules[(state, c)]
        if w == '0':
            ones.remove(cursor)
        if w == '1':
            ones.add(cursor)
        if d == 'right':
            cursor += 1
        if d == 'left':
            cursor -= 1
        state = s

    print('')
    print(len(ones))


with open('input/25') as f:
    lines = f.readlines()

rules, initial, n = parse(lines)
from pprint import pprint
pprint(rules)
print(n)
print(initial)
turing(rules, initial, n)
