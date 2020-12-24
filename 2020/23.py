def rotate(l, n):
    return l[n:] + l[:n]

def play(circle):
    picked_up = circle[1:4]
    rest = circle[4:]
    destination = circle[0] - 1
    while destination in picked_up or destination < min(circle):
        destination -= 1
        if destination < min(circle):
            destination = max(circle)
    destination_index = rest.index(destination)
    new = [circle[0]] + rest[:destination_index+1] + picked_up + rest[destination_index+1:]
    return rotate(new, 1)

#circle = list(map(int, '389125467'))
circle = list(map(int, '158937462'))
for _ in range(100):
    circle = play(circle)

one = circle.index(1)
print(''.join(map(str, rotate(circle, one)[1:])))

