from collections import defaultdict
from functools import lru_cache
import sys
import re

def parse(f):
    rules = defaultdict(list)
    for line in f:
        a, b = line.rstrip().split(' contain ', 1)
        parent = re.sub(' bags', '', a)
        if b == 'no other bags.':
            rules[parent] = []
        else:
            for part in b.split(', '):
                match = re.match(r'(\d+) (.*) bags?.?$', part)
                if match:
                    count = int(match.group(1))
                    color = match.group(2).rstrip()
                else:
                    print('bug')
                rules[parent].append((count, color))

    return dict(rules)

def search(target, rules):
    #@lru_cache(maxsize=1024)
    def count_bags(bag_color: str) -> int:
        s = 0
        for count, color in rules[bag_color]:
            s += count * count_bags(color)
        return s + 1
    return count_bags(target) - 1
    

rules = parse(sys.stdin)
for key, value in rules.items():
    print("'{}' <- {}".format(key, value))
print(search('shiny gold', rules))
