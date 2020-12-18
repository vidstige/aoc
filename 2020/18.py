import operator
import sys
import re

#  expr -> factor * expr | factor
#  factor -> term + factor | term
#  term -> NUMBER | ( expr )

def maybe(f, value):
    try:
        return f(value)
    except ValueError:
        return value

# lexer subsystem
def lex(s):
    tokens = re.split(r'\s*([\\(\)+*])\s*', s)
    # remove empty entries and maybe parse to int
    return [maybe(int, token) for token in tokens if token]

def parse_term(tokens, i):
    #print('term', tokens[i])
    if isinstance(tokens[i], int):
        return tokens[i], i + 1
    assert tokens[i] == '('
    expr, j = parse_expression(tokens, i + 1)
    assert tokens[j] == ')', tokens[j]
    return expr, j + 1

def parse_factor(tokens, i):
    #print('factor', tokens[i])
    term, j = parse_term(tokens, i)
    if j == len(tokens):
        return term, j
    if tokens[j] == '+':
        rhs, j = parse_factor(tokens, j + 1)
        return term + rhs, j
    return term, j


def parse_expression(tokens, i):
    #print('expression', tokens[i])
    factor, j = parse_factor(tokens, i)
    if j == len(tokens):
        return factor, j
    if tokens[j] == '*':
        rhs, j = parse_expression(tokens, j + 1)
        return factor * rhs, j
    return factor, j

def evaluate(line):
    tokens = lex(line)
    ast, _ = parse_expression(tokens, 0)
    return ast

for line in sys.stdin:
    #print(line.strip(), '=', evaluate(line))
    print(evaluate(line))
