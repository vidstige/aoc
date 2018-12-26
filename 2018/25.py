def load(filename):
    with open(filename) as f:
        for line in f:
            yield tuple(map(int, line.split(',')))


def manhattan(a, b):
    n = min(len(a), len(b))
    return sum(abs(a[i] - b[i]) for i in range(n))

def find_constellations(stars):
    while stars:
        constellation = [stars.pop()]
        while True:
            #print(constellation)
            rm = set()
            for b in stars:
                if any(manhattan(a, b) <= 3 for a in constellation):
                    #print(constellation, b)
                    rm.add(b)
            if not rm:
                break
            for star in rm:
                constellation.append(star)
                stars.remove(star)
            #print(constellation)
        yield constellation
        
def main(filename):
    stars = list(load(filename))
    print(len(list(find_constellations(stars))))

main('input/25ex0')
main('input/25ex1')
main('input/25')
