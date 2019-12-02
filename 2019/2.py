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


p = load()
p[1] = 12
p[2] = 2

#p = parse('1,1,1,4,99,5,6,0,99')
print(p)
run(p)
print(p[0])
