ex = {
    1: 0,
    12: 3,
    23: 2,
    1024: 31,
    277678: None
}

def spiral(n):
    x = 0
    y = 0

    dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    
    #m = [[0 for x in range(n)] for y in range(n)]

    d = 0  # direction. index to dirs array
    i = 0  # current number
    s = 0  # segment length so far
    l = 1  # wanted segment length
    while i < n - 1:
        i += 1
        
        #m[y][x] = i

        dx, dy = dirs[d]
        x += dx
        y += dy
        s += 1
        
        if s >= l:
            s = 0
            if d == 0:  # when finishing "right"
                pass
            if d == 1:  # when finishing "down"
                l += 1
            if d == 2:  # when finishing "left"
                pass
            if d == 3:  # when finishing "up"
                l += 1
            d = (d + 1) % len(dirs)

    #return (x, y)
    return abs(x) + abs(y)

#def sum_diag(s, n):
#    diag1 = sum([s[i][i] for i in range(n)])
#    diag2 = sum([s[i][n-1-i] for i in range(n)])
#    return diag1 + diag2 - s[n // 2][n // 2]


for n in ex:
    s = spiral(n)
    print("dist({}) == {}, should be {}".format(n, s, ex[n]))

