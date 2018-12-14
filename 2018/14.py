def main(scoreboard, after, last=10):
    n = last + after - len(scoreboard)
    elves = [0, 1]
    for _ in range(n):
        #print(scoreboard)
        scoreboard += str(sum(int(scoreboard[e]) for e in elves))
        elves = [(e + int(scoreboard[e]) + 1) % len(scoreboard) for e in elves]
    return scoreboard[after:after+last]

print(main('37', 5), '0124515891')
print(main('37', 9), '5158916779')
print(main('37', 18), '9251071085')
print(main('37', 2018), '5941429882')

print(main('37', 920831))
