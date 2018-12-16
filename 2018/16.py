import re
from typing import Tuple

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
    def __init__(self, registers=None, opcode_transform=None):
        self.registers = registers or [0, 0, 0, 0]
        self.transform = opcode_transform
    
    def execute(self, instruction: Tuple[int, int, int, int]) -> None:
        opcode, a, b, c = instruction
        if self.transform:
            opcode = self.transform[opcode]
        CPU.instructions[opcode](self.registers, a, b, c)

def load(filename):
    samples = []
    with open(filename) as f:
        while f:
            m = re.match(r'Before:\s+\[(\d+), (\d+), (\d+), (\d+)\]', f.readline())
            if not m:
                break
            before = [int(x) for x in m.groups()]
            instruction = [int(x) for x in f.readline().split()]
            m = re.match(r'After:\s+\[(\d+), (\d+), (\d+), (\d+)\]', f.readline())
            after = [int(x) for x in m.groups()]
            samples.append((before, instruction, after))
            f.readline()
        
        program = []
        for line in f:
            instruction = tuple(int(x) for x in line.split())
            if len(instruction) == 4:
                program.append(instruction)

    return samples, program

def part1():
    samples, _ = load('input/16ex')
    result = []
    for before, sample, after in samples:
        print(sample)
        count = 0
        for instr in CPU.instructions:
            registers=list(before)
            _, a, b, c = sample
            instr(registers, a, b, c)
            if registers == after:
                count += 1
        result.append(count)

    print(sum(1 for x in result if x >= 3))

def main():
    samples, program = load('input/16')
    possibilities = []
    for _ in range(len(CPU.instructions)):
        possibilities.append(set(range(len(CPU.instructions))))

    for before, sample, after in samples:
        x, a, b, c = sample
        for opcode in range(len(CPU.instructions)):
            cpu = CPU(registers=list(before))
            cpu.execute((opcode, a, b, c))
            if cpu.registers != after:
                possibilities[x].discard(opcode)
    
    assignments = {}
    while any(p for p in possibilities):
        for opcode, ps in enumerate(possibilities):
            if len(ps) == 0 and opcode not in assignments:
                raise Exception('Unsolvable!')
            if len(ps) == 1:
                i = next(iter(ps))
                assignments[opcode] = i
                for s in possibilities:
                    s.discard(i)
    
    cpu = CPU(opcode_transform=assignments)
    for instruction in program:
        cpu.execute(instruction)
    print(cpu.registers)

main()

