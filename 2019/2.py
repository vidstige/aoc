def parse(s):
    return [int(i) for i in s.split(',')]
    
def load():
    with open('input/2') as f:
        return parse(f.read())

def run(program):
    ip = 0
    while program[ip] != 99:
        a = program[ip + 1]
        b = program[ip + 2]
        destination = program[ip + 3]
        if program[ip] == 1:
            program[destination] = program[a] + program[b]
        elif program[ip] == 2:
            program[destination] = program[a] * program[b]
        else:
            raise ValueError('bad opcode!' + program[ip])
        ip += 4


def search(needle, program):
    for noun in range(100):
        for verb in range(100):
            p = list(program)
            p[1] = noun
            p[2] = verb
            run(p)
            r = p[0]
            #print('{}, {} ->{}'.format(noun, verb, r))
            if r == needle:
                return noun, verb
            
    
program = load()

noun, verb = search(19690720, program)
print(100 * noun + verb)
