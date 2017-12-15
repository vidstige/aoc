from itertools import islice, count

def generate(seed, multiplier, stride=1):
    x = seed
    for _ in count():
        x = (x * multiplier) % 2147483647
        if x % stride == 0:
            yield x

def judge(A, B, n):
    c = 0
    for a, b in islice(zip(A, B), n):
        #print("{} \t{}".format(a,b))
        if a & 0xffff == b & 0xffff:
            c += 1
    return c

print(judge(generate(65, 16807, stride=4), generate(8921, 48271, stride=8), n=5))
print(judge(
    generate(618, 16807, stride=4),
    generate(814, 48271, stride=8),
    n=5000000))
#matching = generate(618, 814, n=40 * 1000000)
#print(sum(1 for _ in matching))

