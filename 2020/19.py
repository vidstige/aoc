import sys


class Rule:
    def match(self, rules, tokens, i):
        pass


class Literal(Rule):
    def __init__(self, literal):
        self.literal = literal
    
    def match(self, rules, tokens, i):
        del rules
        j = i + len(self.literal)
        if tokens[i:j] == self.literal:
            return j
        return i

    def __repr__(self):
        return "Literal({literal})".format(literal=repr(self.literal))


class Sequence(Rule):
    def __init__(self, sequence):
        self.sequence = sequence

    def match(self, rules, tokens, i):
        j = i
        for name in self.sequence:
            rule = rules[name]
            k = rule.match(rules, tokens, j)
            if k > j:
                j = k
            else:
                return i
        return j

    def __repr__(self):
        return "Sequence({literal})".format(literal=repr(self.sequence))


class Either(Rule):
    def __init__(self, sequence):
        self.sequence = sequence
    
    def match(self, rules, tokens, i):
        for rule in self.sequence:
            j = rule.match(rules, tokens, i)
            if j > i:
                return j
        #assert False, "Nothing matched, expected one of {}".format(self.sequence)
        return i

    def __repr__(self):
        return "Either({literal})".format(literal=repr(self.sequence))


def segments(f):
    """Returns segments of a file, separated by newline"""
    parts = [[]]
    for line_n in f:
        line = line_n.strip()
        if line:
            parts[-1].append(line)
        else:
            parts.append([])
    return tuple(parts)


def parse_rules(lines):
    rules = {}
    for line in lines:
        name, rest = line.split(': ', 1)
        if rest.startswith('"') and rest.endswith('"'):
            rules[name] = Literal(rest.strip('"'))
        else:
            either = rest.split('|')
            if len(either) > 1:
                rules[name] = Either([Sequence(e.split()) for e in either])
            else:
                rules[name] = Sequence(rest.split())
    return rules


def matches(rules, tokens):
    root = rules['0']
    return root.match(rules, tokens, 0) == len(tokens)


rule_lines, messages = segments(sys.stdin)
rules = parse_rules(rule_lines)
#print(rules)
for message in messages:
    if matches(rules, message):
        print(message)
    
