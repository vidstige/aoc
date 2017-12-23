class chip(object):
    def __init__(self, program, initial=None):
        self.program = program.splitlines()
        self.ip = 0
        self.cpu = initial or {}
        self.stats = 0

    def evaluate(self, o):
        try:
            return int(o)
        except ValueError:
            pass
        return self.cpu.get(o, 0)

    def execute(self, line):
        cpu = self.cpu
        evaluate = self.evaluate

        parts = line.split()
        if len(parts) == 2:
            parts.append(None)
        opcode, register, operand = parts

        if opcode == "set":
            cpu[register] = evaluate(operand)
            return 1
        if opcode == "sub":
            cpu[register] = cpu.get(register, 0) - evaluate(operand)
            return 1
        if opcode == "mul":
            cpu[register] = cpu.get(register, 0) * evaluate(operand)
            return 1

        if opcode == "jnz":
            return evaluate(operand) if evaluate(register) != 0 else 1

    def step(self):
        if not self.alive():
            return

        self.ip += self.execute(self.program[self.ip])

    def alive(self):
        return self.ip >= 0 and self.ip < len(self.program)

    def debug(self, ip=None):
        parts = self.program[self.ip if ip is None else ip].split()
        if len(parts) == 2:
            parts.append(None)
        opcode, register, operand = parts
        return (self.evaluate(register), '' if operand is None else self.evaluate(operand))


def render(data, chips, backup):
    def fmt(i, c, line):
        a, b = c.debug(i)
        return "{}{: <16} {: >12}{: >12}".format(">" if c.ip == i else " ", line, a, b)

    if backup:
        for _ in data:
            print("\033[F", end='')

    for i, line in enumerate(data):
        print("{:02}  {}".format(i, "  ".join(fmt(i, c, line) for c in chips)))

def run(data, initial):
    c = chip(data, initial)
    while c.alive():
        c.step()

    print(c.cpu.get('h'))


def dbg(data, initial):
    c = chip(data, initial)
    skip = 0
    while c.alive():
        c.step()

        if skip == 0:
            render(data.splitlines(), [c], True)

            print("\033[F", end='')
            debug = input()
            if debug:
                cmd, d = debug.split(' ', 1)
                if cmd == 'p':
                    #print(c.evaluate(d))
                    print(c.cpu)
                    input()
                if cmd == 'r':
                    skip = int(d)
                if cmd == 'j':
                    c.ip += int(d)
                if cmd == 'e':
                    c.execute(d)
        else:
            skip -= 1
                

    #print(c.stats)

#dual(ex2)
with open('input/23') as f:
    #run(f.read(), {'a': 0})
    dbg(f.read(), {'a': 0})
