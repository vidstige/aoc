import sys
import re
from itertools import product

def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def expand(adress, floats, on):
    a = adress | on
    for float_values in product((clear_bit, set_bit), repeat=len(floats)):
        for bit, f in zip(floats, float_values):
            a = f(a, bit)
        yield a


mask = None
on = 0
floats = []
mem = {}
for line in sys.stdin:
    match = re.match(r'mask = ([10X]{36})', line)
    if match:
        mask = match.group(1)
        floats = [i for i, mi in enumerate(reversed(mask)) if mi == 'X']
        #print(mask, floats)
        on = int(mask.replace('X', '0'), 2)

    match = re.match(r'mem\[(\d+)\] = (\d+)', line)
    if match:
        adress, value = int(match.group(1)), int(match.group(2))
        #bin_value = bin(value)[2:].zfill(36)
        #assert int(bin_value, 2) == value
        #masked = ''.join([vi if mi == 'X' else mi for vi, mi in zip(bin_value, mask)])
        #mem[adress] = int(masked, 2)
        for adress in expand(adress, floats, on):
            mem[adress] = value

#for i, value in sorted(mem.items()):
#    print('{:05}: {}'.format(i, value))

print(sum(mem.values()))
