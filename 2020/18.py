import operator
import sys
import re

#expr = operand + expr | operand * expr | operand
# operand = number | ( expr)

OPERATORS = {
    '+': operator.add, '*': operator.mul
}

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

# recursive decent parser subsystem
def parse_operand(tokens, i):
    token = tokens[i]
    if isinstance(token, int):
        return token, i + 1
    if tokens[i] == '(':
        tmp, j = parse_expression(tokens, i + 1)
        assert tokens[j] == ')'
        return tmp, j + 1
    # special hack for left recursion -_-
    # don't consume anything
    return None, i

def parse_expression(tokens, i):
    operand, j = parse_operand(tokens, i)
    if j == len(tokens):
        return operand, j
    operator = OPERATORS.get(tokens[j])
    # special hack to handle left recursion -_-
    while operator:
        j += 1  # consume operator
        # try parsing operand
        maybe_operand, j = parse_operand(tokens, j)
        if maybe_operand:
            rhs = maybe_operand
        else:
            print('erroids')
            rhs, j = parse_expression(tokens, j)
        operand = operator(operand, rhs)
        operator = OPERATORS.get(tokens[j]) if j < len(tokens) else None
    return operand, j

def evaluate(line):
    tokens = lex(line)
    ast, _ = parse_expression(tokens, 0)
    return ast

for line in sys.stdin:
    print(evaluate(line))
