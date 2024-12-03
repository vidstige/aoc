import re
import sys

program = sys.stdin.read()
pattern = re.compile(r"mul\((\d+),(\d+)\)|(don't|do)")

total = 0
enabled = True
for a, b, op in re.findall(pattern, program):
    if op == "do":
        enabled = True
    if op == "don't":
        enabled = False
    if enabled and a and b:
        total += int(a) * int(b)
print(total)
