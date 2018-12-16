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
    def __init__(self, registers=None):
        self.registers = registers or [0, 0, 0, 0]
    
    def execute(self, instruction: Tuple[int, int, int, int]) -> None:
        opcode, a, b, c = instruction
        CPU.instructions[opcode](self.registers, a, b, c)

def load(filename):
    with open(filename) as f:
        while f:
            m = re.match(r'Before:\s+\[(\d+), (\d+), (\d+), (\d+)\]', f.readline())
            if not m:
                return
            before = [int(x) for x in m.groups()]
            instruction = [int(x) for x in f.readline().split()]
            m = re.match(r'After:\s+\[(\d+), (\d+), (\d+), (\d+)\]', f.readline())
            after = [int(x) for x in m.groups()]
            yield before, instruction, after
            f.readline()

result = []
for before, instruction, after in load('input/16'):
    print(instruction)
    count = 0
    for instr in CPU.instructions:
        registers=list(before)
        _, a, b, c = instruction
        instr(registers, a, b, c)
        if registers == after:
            count += 1
    result.append(count)

print(sum(1 for x in result if x >= 3))
