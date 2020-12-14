import sys
import re

mask = None
mem = {}
for line in sys.stdin:
    match = re.match(r'mask = ([10X]{36})', line)
    if match:
        mask = match.group(1)
    match = re.match(r'mem\[(\d+)\] = (\d+)', line)
    if match:
        adress, value = int(match.group(1)), int(match.group(2))
        bin_value = bin(value)[2:].zfill(36)
        assert int(bin_value, 2) == value
        masked = ''.join([vi if mi == 'X' else mi for vi, mi in zip(bin_value, mask)])
        mem[adress] = int(masked, 2)

#for i, value in sorted(mem.items()):
#    print('{:05}: {}'.format(i, value))

print(sum(mem.values()))
