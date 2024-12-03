import re
import sys

program = sys.stdin.read()
pattern = re.compile(r'mul\((\d+),(\d+)\)')

total = sum(int(a) * int(b) for a, b in re.findall(pattern, program))
print(total)
