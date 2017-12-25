import re 

def parse(lines):
    def direction(s):
        if s == 'left':
            return -1
        if s == 'right':
            return 1
        raise ValueError("Unknown direction: {}".format(s))
    def bit(s):
        if s == '0':
            return False
        if s == '1':
            return True
        raise ValueError("Unknown bit: {}".format(s))
    def transition(j):
        w = bit(re.search('([01])', lines[j]).group(1))
        d = direction(re.search('(left|right)', lines[j+1]).group(1))
        s = re.search('state ([A-Z])', lines[j+2]).group(1)
        return w, d, s

    n = (len(lines) - 3) // 10
    i = 0

    initial = re.match('Begin in state ([A-Z])\.', lines[0]).group(1)
    steps = int(re.search('(\d+)', lines[1]).group(1))

    rules = {}
    for i in range(n+1):
        i = 3 + i * 10
        state = re.match('In state ([A-Z]):', lines[i]).group(1)

        current = bit(re.search('([01])', lines[i+1]).group(1))
        rules[(state, current)] = transition(i + 2)

        current = bit(re.search('([01])', lines[i+5]).group(1))
        rules[(state, current)] = transition(i + 6)

    return rules, initial, steps

def turing(rules, initial, n):
    ones = set()
    cursor = 0
    state = initial

    for i in range(n):
        if i % 50001 == 0:
            print("\r{}".format(100*i // n), end='')

        w, d, state = rules[(state, cursor in ones)]
        (ones.add if w else ones.remove)(cursor)
        cursor += d

    print('')

    return ones

def main():
    with open('input/25') as f:
        lines = f.readlines()

    rules, initial, n = parse(lines)
    print(len(turing(rules, initial, n)))

main()
