def valid(pin):
    p = str(pin)
    count = 0
    double = False
    for a, b in zip(p[:-1], p[1:]):
        if a == b:
            count += 1
        else:
            if count == 1:
                double = True
            count = 0
        if a > b:
            return False
    if count == 1:
        double = True
    return double
        
def search(a, b):
    return [pin for pin in range(a, b + 1) if valid(pin)]

print(len(search(130254, 678275)))
#print(valid('112233'))