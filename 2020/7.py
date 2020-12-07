from collections import defaultdict
import sys
import re

def parse(f):
    rules = defaultdict(list)
    for line in f:
        a, b = line.rstrip().split(' contain ', 1)
        parent = re.sub(' bags', '', a)
        if b == 'no other bags.':
            pass
        else:
            for part in b.split(', '):
                match = re.match(r'(\d+) (.*) bags?.?$', part)
                if match:
                    count = int(match.group(1))
                    color = match.group(2)
                else:
                    print('bug')
                rules[color.rstrip()].append((count, parent))
            #print(b.split(', '))

        #match = re.match(r'^([a-z ]+ bags) contain (\d+ [a-z ]+ bags?)+', line)
        #if match:
        #    print(line)
        #    print(match.groups())
        #    matches = iter(match.groups())
        #    parent = re.sub(r'bags?$', '', next(matches)).rstrip()
        #    for group in matches:
        #        if group is None:
        #            continue
        #        child = re.sub(r'^,?\s?', '', re.sub(r'bags?$', '', group))
        #        count, color = child.split(' ', 1)
        #        rules[color.rstrip()].append((count, parent))
        #else:
        #    print(line)
        #match = re.match(r'^([a-z ]+) bags contain no other bags', line)
        #if match:
        #    print(match.groups(1))
    return dict(rules)

def search(target, rules):
    targets = [target]
    visited = set()
    while targets:
        color = targets.pop(-1)
        visited.add(color)
        for _, color in rules.get(color, []):
            targets.append(color)
    visited.remove(target)
    #print(visited)
    return len(visited)

rules = parse(sys.stdin)
#for key, value in rules.items():
#    print("'{}' <- {}".format(key, value))
# 188 - too low
print(search('shiny gold', rules))