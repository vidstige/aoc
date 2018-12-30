import re
from typing import List, Tuple

def addr(registers, a, b, c):
    registers[c] = registers[a] + registers[b]

def addi(registers, a, b, c):
    registers[c] = registers[a] + b

def mulr(registers, a, b, c):
    registers[c] = registers[a] * registers[b]

def muli(registers, a, b, c):
    registers[c] = registers[a] * b

def banr(registers, a, b, c):
    registers[c] = registers[a] & registers[b]

def bani(registers, a, b, c):
    registers[c] = registers[a] & b

def borr(registers, a, b, c):
    registers[c] = registers[a] | registers[b]

def bori(registers, a, b, c):
    registers[c] = registers[a] | b

def setr(registers, a, b, c):
    registers[c] = registers[a]

def seti(registers, a, b, c):
    registers[c] = a

def gtir(registers, a, b, c):
    registers[c] = 1 if a > registers[b] else 0
    
def gtri(registers, a, b, c):
    registers[c] = 1 if registers[a] > b else 0
    
def gtrr(registers, a, b, c):
    registers[c] = 1 if registers[a] > registers[b] else 0

def eqir(registers, a, b, c):
    registers[c] = 1 if a == registers[b] else 0
    
def eqri(registers, a, b, c):
    registers[c] = 1 if registers[a] == b else 0
    
def eqrr(registers, a, b, c):
    registers[c] = 1 if registers[a] == registers[b] else 0


Instruction = Tuple[str, int, int, int]


def draw(program: List[Instruction], ip: int) -> None:
    for i, instruction in enumerate(program):
        opcode, a, b, c = instruction
        print("{:02} {} {} {} {} {:>12}".format(
            i, opcode, a, b, c,
            '<--' if i == ip else ''))


class CPU(object):
    instructions = [
        addr, addi,
        mulr, muli,
        banr, bani,
        borr, bori,
        setr, seti,
        gtir, gtri, gtrr,
        eqir, eqri, eqrr
    ]
    def __init__(self, ip=None, registers=None):
        register_count = 6
        self.ip = ip
        #self.registers = registers or [0] * register_count
        self.registers = registers
        self.lookup = {f.__name__: f for f in CPU.instructions}
    
    def execute(self, instruction: Instruction) -> None:
        opcode, a, b, c = instruction
        self.lookup[opcode](self.registers, a, b, c)

    def run(self, program: List[Instruction]) -> None:
        ip = 0
        while ip >= 0 and ip < len(program):
            self.registers[self.ip] = ip
            self.execute(program[ip])
            ip = self.registers[self.ip]
            ip +=1
            draw(program, ip)
            input()

def load(filename):
    with open(filename) as f:
        for line in f:
            match = re.match(r'#ip \d', line)
            if match:
                pass
            else:
                opcode, a, b, c = line.split()
                yield opcode, int(a), int(b), int(c)

def main():
    program = list(load('input/21'))
    cpu = CPU(ip=1, registers=[0, 0, 0, 0, 0, 0])
    cpu.run(program)
    print(cpu.registers)

main()

