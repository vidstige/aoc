def load():
    with open('input/16') as f:
        return f.read()

def pattern(x, y):
    i = (x - y) // (y + 1) + 1
    if i < 0:
        return 0
    return (0, 1, 0, -1)[i % 4]

def phase(signal):
    result = ''
    for i, _ in enumerate(signal):
        tmp = sum(int(s) * pattern(j, i) for j, s in enumerate(signal))
        result += str(abs(tmp) % 10)
    return result

def fft(signal, phases, first=8):
    for _ in range(phases):
        signal = phase(signal)
    return signal[:first]

print(fft('80871224585914546619083218645595', phases=100))
print(fft('19617804207202209144916044189917', phases=100))
print(fft('69317163492948606335995924319873', phases=100))
print(fft(load(), phases=100))
