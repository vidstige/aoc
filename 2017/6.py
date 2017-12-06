def reallocate(memory):
    selected = memory.index(max(memory))
    tmp = list(memory)
    redist = tmp[selected]
    tmp[selected] = 0

    n = selected + 1
    while redist > 0:
        tmp[n % len(tmp)] += 1
        redist -= 1
        n += 1

    return tuple(tmp)


def count(initial):
    history = set()
    memory = initial
    c = 0
    while memory not in history:
        history.add(memory)
        print(memory)
        memory = reallocate(memory)
        c += 1
    return c


def count_inf(initial):
    history = set()
    memory = initial
    
    # find the first repeating
    while memory not in history:
        history.add(memory)
        memory = reallocate(memory)
    
    # forget all states
    history = set()
    c = 0
    while memory not in history:
        history.add(memory)
        memory = reallocate(memory)
        c += 1
    
    return c

print(count_inf((0, 2, 7, 0)))

data = "5	1	10	0	1	7	13	14	3	12	8	10	7	12	0	6"
print(count(tuple(int(x) for x in data.split())))
print(count_inf(tuple(int(x) for x in data.split())))
