import sys

groups = sys.stdin.read().split('\n\n')
print(sum(len(set("".join(group.split()))) for group in groups))
