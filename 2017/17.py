def spinlock(n):
    buffer = [0]
    p = 0

    for i in range(0, 2017):
        p = (p + 3) % len(buffer)
        p += 1
        buffer.insert(p, i+1)

    return buffer, p

def main():
    buffer, p = spinlock(3)
    print(buffer[p+1])
    

main()