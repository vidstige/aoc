from dataclasses import dataclass, astuple, replace as copy
from itertools import count
import re
import sys
from typing import TextIO

@dataclass
class Registers:
    a: int
    b: int
    c: int

def parse_register(register: str, line: str):
    match = re.match(r"Register ([A-Z]): (\d+)", line)
    assert match.group(1) == register
    return int(match.group(2))

def parse_program(line: str) -> bytes:
    return bytes(int(match.group(0)) for match in re.finditer("\d+", line))

def parse(f: TextIO) -> tuple[bytes, Registers]:
    a = parse_register('A', f.readline())
    b = parse_register('B', f.readline())
    c = parse_register('C', f.readline())
    f.readline()  # blank
    program = parse_program(f.readline())
    registers=Registers(a=a, b=b, c=c)
    return program, registers

def combo(operand: int, registers: Registers) -> int:
    if operand < 4:
        return operand
    if operand == 4:
        return registers.a
    if operand == 5:
        return registers.b
    if operand == 6:
        return registers.c
    assert False, f"unexpected operand: {operand}"

def adv(operand: int, registers: Registers, _: bytearray):
    registers.a = registers.a // (1 << combo(operand, registers))
def bxl(operand: int, registers: Registers, _: bytearray):
    registers.b = registers.b ^ operand
def bst(operand: int, registers: Registers, _: bytearray):
    registers.b = combo(operand, registers) % 8
def jnz(operand: int, registers: Registers, _: bytearray):
    return operand if registers.a else None
def bxc(operand: int, registers: Registers, _: bytearray):
    registers.b = registers.b ^ registers.c
def out(operand: int, registers: Registers, output: bytearray):
    value = combo(operand, registers) % 8
    output.append(value)
def bdv(operand: int, registers: Registers, _: bytearray):
    registers.b = registers.a // (1 << combo(operand, registers))
def cdv(operand: int, registers: Registers, _: bytearray):
    registers.c = registers.a // (1 << combo(operand, registers))

OPCODES = [
    adv,
    bxl,
    bst,
    jnz,
    bxc,
    out,
    bdv,
    cdv,
]
def run(
    program: bytes,
    registers: Registers,
    ip: int = 0,
    bail: bool = False,
) -> bytes | None:
    output = bytearray()
    while ip < len(program):
        if bail and not program.startswith(output):
            return None  # abort
        #key = (astuple(registers), ip)
        #if key in cache:
        #    return cache[key]
        opcode = program[ip]
        operand = program[ip+1]
        #print(f"{ip:03d} {OPCODES[opcode].__name__} {operand}")
        jmp = OPCODES[opcode](operand, registers, output)
        ip = ip + 2 if jmp is None else jmp
    #cache[(astuple(registers), ip)] = bytes(output)
    return bytes(output)

program, registers = parse(sys.stdin)
output = run(program, copy(registers))
# 1
print(','.join(str(o) for o in output))

for a in count():
    if a % 100000 == 0:
        print(a)
    r = copy(registers)
    r.a = a
    output = run(program, r, bail=True)
    if output == program:
        print(a)
        break