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


data = load('input/8')
print(sum(metadata(data)))
