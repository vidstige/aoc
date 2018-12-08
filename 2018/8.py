def load(path):
    with open(path) as f:
        return [int(x) for x in f.read().split()]

def metadata(data):
    n = data.pop(0)
    metadata_count = data.pop(0)
    for _ in range(n):
        yield from metadata(data)
    for _ in range(metadata_count):
        yield data.pop(0)

def value(data):
    n = data.pop(0)
    m = data.pop(0)

    childs = [value(data) for _ in range(n)] if n else []
    metadata = [data.pop(0) for _ in range(m)]
    if n:
        return sum(childs[i-1] for i in metadata if i-1 in range(len(childs)))
    return sum(metadata)

data = load('input/8')
#print(sum(metadata(data)))
print(value(data))
