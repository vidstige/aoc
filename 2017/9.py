count_examples = {
    '{}': 1,
    '{{{}}}': 3,
    '{{},{}}': 3,
    '{{{},{},{{}}}}': 6,
    '{<{},{},{{}}>}': 1,
    '{<a>,<a>,<a>,<a>}': 1,
    '{{<a>},{<a>},{<a>},{<a>}}': 5,
    '{{<!>},{<!>},{<!>},{<a>}}': 2
}

score_examples = {
    '{}': 1,
    '{{{}}}': 6,
    '{{},{}}': 5,
    '{{{},{},{{}}}}': 16,
    "{<a>,<a>,<a>,<a>}": 1,
    "{{<ab>},{<ab>},{<ab>},{<ab>}}": 9,
    '{{<!!>},{<!!>},{<!!>},{<!!>}}': 9,
    "{{<a!>},{<a!>},{<a!>},{<ab>}}": 3
}

def score(stream):
    gn = 0  # nesting level
    garbage = False
    escape = False  # skip next character
    score = []
    garbage_size = 0
    for c in stream:
        if escape:
            escape = False
            continue

        if garbage:
            if c == '!':
                escape = True
            elif c == '>':
                garbage = False
            else:
                garbage_size += 1
        else:
            if c == '{':
                gn += 1
            if c == '}':
                score.append(gn)
                gn -= 1
            if c == '<':
                garbage = True
    return score, garbage_size


for example, expected in count_examples.items():
    s, _ = score(example)
    actual = sum(1 for _ in s)
    if actual == expected:
        print('✔ {}'.format(example))
    else:
        print('Expected {} but got {} for {}'.format(expected, actual, example))


for example, expected in score_examples.items():
    s, _ = score(example)
    actual = sum(s)
    if actual == expected:
        print('✔ {}'.format(example))
    else:
        print('Expected {} but got {} for {}'.format(expected, actual, example))


with open('input/9') as f:
    data = f.read()
    s, gc = score(data)
    print(sum(s))
    print(gc)
