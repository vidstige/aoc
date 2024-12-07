import sys

def parse(f):
    for line in f:
        raw_test_value, raw_parts = line.rstrip().split(':')
        parts = raw_parts.split()
        values = [int(v) for v in parts]
        yield values, int(raw_test_value)

def add(a: int, b: int) -> int:
    return a + b

def mul(a: int, b: int) -> int:
    return a * b

def join(a: int, b: int) -> int:
    return int(str(a) + str(b))

def search(values: list[int], test_value: int, operators: list):
    if len(values) == 1:
        return test_value == values[0]

    results = []
    for operator in operators:
        rest = values.copy()
        a = rest.pop(0)
        b = rest.pop(0)
        rest.insert(0, operator(a, b))
        results.append(search(rest, test_value, operators))

    return any(results)


a, b = 0, 0
for values, test_value in parse(sys.stdin):
    if search(values, test_value, (add, mul)):
        a += test_value
    if search(values, test_value, (add, mul, join)):
        b += test_value

print(a)
print(b)
