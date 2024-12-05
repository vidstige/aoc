from functools import cmp_to_key
import sys


def parse(f):
    rules = []
    for line in f:
        line = line.rstrip()
        if not line:
            break
        a, b = line.split('|')
        rules.append((int(a), int(b)))
    book = []
    for line in f:
        pages = [int(page) for page in line.rstrip().split(',')]
        book.append(pages)
    return rules, book

def compare(rules, a, b):
    for x, y in rules:
        if x == a and y == b:
            return -1
        if x == b and y == a:
            return 1
    return 0

rules, book = parse(sys.stdin)
first_star, second_star = 0, 0
for pages in book:
    correct = list(sorted(pages, key=cmp_to_key(lambda a, b: compare(rules, a, b))))
    mid = correct[len(pages) // 2]
    if correct == pages:
        first_star += mid
    else:
        second_star += mid

print(first_star)
print(second_star)