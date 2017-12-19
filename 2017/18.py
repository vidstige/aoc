ex = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

ex2 = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""

data = """set i 31
set a 1
mul p 17
jgz p p
mul a 2
add i -1
jgz i -2
add a -1
set i 127
set p 680
mul p 8505
mod p a
mul p 129749
add p 12345
mod p a
set b p
mod b 10000
snd b
add i -1
jgz i -9
jgz a 3
rcv b
jgz b -1
set f 0
set i 126
rcv a
rcv b
set p a
mul p -1
add p b
jgz p 4
snd a
set a b
jgz 1 3
snd b
set f 1
add i -1
jgz i -11
snd a
jgz f -16
jgz a -19"""

class chip(object):
    def __init__(self, program, program_id, pipe_in, pipe_out):
        self.program = program.splitlines()
        self.ip = 0
        self.cpu = {'p': program_id}
        self.pipe_in = pipe_in
        self.pipe_out = pipe_out
        self.blocked = False
        
        self.stats = 0

    def evaluate(self, o):
        try:
            return int(o)
        except ValueError:
            pass
        return self.cpu.get(o, 0)
        

    def step(self):
        if not self.alive():
            return
        cpu = self.cpu
        evaluate = self.evaluate

        #print(self.program[self.ip])

        parts = self.program[self.ip].split()
        if len(parts) == 2:
            parts.append(None)
        opcode, register, operand = parts
        
        if opcode == "set":
            cpu[register] = evaluate(operand)
            self.ip += 1
        if opcode == "add":
            cpu[register] = cpu.get(register, 0) + evaluate(operand)
            self.ip += 1
        if opcode == "mul":
            cpu[register] = cpu.get(register, 0) * evaluate(operand)
            self.ip += 1
        if opcode == "mod":
            cpu[register] = cpu.get(register, 0) % evaluate(operand)
            self.ip += 1

        if opcode == "snd":
            value = evaluate(register)
            self.pipe_out.append(value)
            self.stats += 1
            self.ip += 1

        if opcode == "rcv":
            #if cpu.get(register, 0) == 0:
            #    self.ip += 1
            #else:
            if self.pipe_in:
                self.blocked = False
                cpu[register] = self.pipe_in.pop(0)
                self.ip += 1
            else:
                self.blocked = True

        if opcode == "jgz":
            if evaluate(register) > 0:
                self.ip += evaluate(operand)
            else:
                self.ip += 1

        if any(key not in 'abcifp' for key in self.cpu):
            print("UH OH")
            print(self.cpu)

    def alive(self):
        return self.ip >= 0 and self.ip < len(self.program)

    def debug(self, ip=None):
        parts = self.program[self.ip if ip is None else ip].split()
        if len(parts) == 2:
            parts.append(None)
        opcode, register, operand = parts
        return (self.evaluate(register), '' if operand is None else self.evaluate(operand))


def deadlock(chips):
    return all(c.blocked for c in chips)

def render(data, chips, backup):
    def fmt(i, c, line):
        a, b = c.debug(i)
        return "{}{: <16} {: >12}{: >12}".format(">" if c.ip == i else " ", line, a, b)

    if backup:
        for _ in data:
            print("\033[F", end='')

    for i, line in enumerate(data):
        print("{:02}  {}".format(i, "  ".join(fmt(i, c, line) for c in chips)))


def dual(data):
    forward = list()
    backward = list()
    chips = [chip(data, 0, forward, backward),
             chip(data, 1, backward, forward)]
    
    i = 0
    current = 0
    while any(c.alive() for c in chips) and not deadlock(chips):
        #log = [c.program[c.ip] for c in chips]
        #print("{}".format(" \t".join(log)), end='\n')
        if i % 1001 == 0:
            print("\r{}".format(" \t".join(str(len(c.pipe_in)) for c in chips)), end='')
        #    print("\r{}".format(i), end='')

        #render(data.splitlines(), chips, i>0)
        #print("\033[F", end=''); input()
        #import time; time.sleep(0.1)

        i += 1
        
        #for c in chips:
        #    if c.alive():
        #        c.step()
        chips[current].step()
        if chips[current].blocked:
            current = (current + 1) % 2
            chips[current].step()

    print()
    print(chips[1].stats)
    print("deadlock: {}".format(deadlock(chips)))
    for c in chips:
        print(c.alive())

#print(run(ex.splitlines()))
#print(run(data.splitlines()))

#dual(ex2)
dual(data)
