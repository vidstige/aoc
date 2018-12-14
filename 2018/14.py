def main(scoreboard, after, last=10):
    n = last + after - len(scoreboard)
    elves = [0, 1]
    for _ in range(n):
        #print(scoreboard)
        scoreboard += str(sum(int(scoreboard[e]) for e in elves))
        elves = [(e + int(scoreboard[e]) + 1) % len(scoreboard) for e in elves]
    return scoreboard[after:after+last]

def search(scoreboard, match):
    elves = [0, 1]
    scores = [int(rs) for rs in scoreboard]
    while True:
        scores.extend(int(r) for r in str(sum(scores[e] for e in elves)))
        elves = [(e + scores[e] + 1) % len(scores) for e in elves]

        if match in ''.join(str(x) for x in scores[-len(match)-2:]):
            return len(scores) - len(match)


#print(main('37', 5), '0124515891')
#print(main('37', 9), '5158916779')
#print(main('37', 18), '9251071085')
#print(main('37', 2018), '5941429882')

#print(main('37', 920831))

print(search('37', '01245'), 5)
print(search('37', '51589'), 9)
print(search('37', '92510'), 18)
print(search('37', '59414'), 2018)

print(search('37', '920831'))
