from string import ascii_lowercase, ascii_uppercase

def load():
    with open('input/5') as f:
        return f.read()

def reactions():
    for l, h in zip(ascii_lowercase, ascii_uppercase):
        yield l + h
        yield h + l

def reduc(polymer):
    rs = list(reactions())
    
    p = polymer
    while True:
        old = str(p)
        p = old
        for r in rs:
            p = p.replace(r, '', 1)
        if old == p:
            break
    return p

polymer = load()
print(len(reduc(polymer)))

# part 2
polymer = load()
for r in reactions():
    new = polymer.replace(r[0], '').replace(r[1], '')
    print(r, len(reduc(new)))
