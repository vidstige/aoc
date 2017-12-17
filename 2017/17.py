from tqdm import tqdm

def spinlock(step, n):
    buffer = [0]
    p = 0

    for i in tqdm(range(0, n), mininterval=1):
        p = (p + step) % len(buffer)
        p += 1
        buffer.insert(p, i+1)

    return buffer, p

def main():
    buffer, p = spinlock(382, n=2017)
    print(buffer[p+1])

    buffer, _ = spinlock(382, n=50000000)
    idx = buffer.index(0)
    print(buffer[idx+1])


main()