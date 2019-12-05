def load(day):
    with open('input/{day}'.format(day=day)) as f:
        return [int(x) for x in f.read().split(',')]

def parameter(i, ip, program, modes):
    value = program[ip + i]
    if modes[i] == 0:
        return program[value]
    return value

def run(program, data=None):
    ip = 0
    out = []
    while True:
        opcode = program[ip] % 100
        pm = program[ip] // 100
        ip += 1
        modes = []
        for _ in range(3):
            modes.append(pm % 10)
            pm = pm // 10

        if opcode == 1:
            a = parameter(0, ip, program, modes)
            b = parameter(1, ip, program, modes)
            destination = program[ip + 2]
            print("add", a, b, destination, modes)
            program[destination] = a + b
            ip += 3
        elif opcode == 2:
            a = parameter(0, ip, program, modes)
            b = parameter(1, ip, program, modes)
            destination = program[ip + 2]
            print("mul", a, b, destination, modes)
            program[destination] = a * b
            ip += 3
        elif opcode == 3:
            destination = program[ip]
            program[destination] = data.pop()
            print("read ", program[destination], "to", destination, modes)
            ip += 1
        elif opcode == 4:
            source = program[ip]
            print("write ", program[source], modes)
            out.append(program[source])
            ip += 1
        elif opcode == 99:
            break
        else:
            raise ValueError('bad opcode: {}'.format(opcode))
    return out
