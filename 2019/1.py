def fuel(mass):
    f = mass // 3 - 2
    if f <= 0:
        return 0
    return f + fuel(f)

with open('input/1') as f:
    data = f.readlines()

masses = [int(d) for d in data]
fuels = [fuel(mass) for mass in masses]
print(sum(fuels))
