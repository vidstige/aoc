import sys

def parse(f):
    for line in f:
        raw_test_value, raw_parts = line.rstrip().split(':')
        parts = raw_parts.split()
        values = [int(v) for v in parts]
        yield values, int(raw_test_value)

def pop_two(items: list):
    copy = items.copy()
    a = copy.pop(0)
    b = copy.pop(0)
    return a, b, copy

def search(values: list[int], test_value: int):
    if len(values) == 1:
        return test_value == values[0]
    # add
    a, b, add = pop_two(values)
    add.insert(0, a + b)
    # mul
    a, b, mul = pop_two(values)
    mul.insert(0, a * b)

    return search(add, test_value) or search(mul, test_value)
    
total = 0
for values, test_value in parse(sys.stdin):
    if search(values, test_value):
        total += test_value

print(total)
