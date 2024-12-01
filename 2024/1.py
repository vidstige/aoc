import sys
from collections import Counter

left, right = [], []
for line in sys.stdin:
    l, r = line.split()
    left.append(int(l))
    right.append(int(r))

# 1
print(sum(abs(l - r) for l, r in zip(sorted(left), sorted(right))))

# 
count = Counter(right)
print(sum(l * count.get(l, 0) for l in left))
