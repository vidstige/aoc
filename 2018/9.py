def circle(raw, items):
    return raw % len(items)

def main(player_count, marble_count):
    marbles = [0]
    index = None
    players = [0] * player_count
    for m in range(1, marble_count + 1):
        player = circle(m - 1, players)

        if m % 23 == 0:
            players[player] += m
            index = circle(index - 7, marbles)
            players[player] += marbles.pop(index)
        else:
            if len(marbles) < 2:
                index = len(marbles)
                marbles.append(m)
            else:
                index = circle(index + 2, marbles)
                marbles.insert(index, m)
        
        #print(player, marbles)
    score, winner = max((s, i) for i, s in enumerate(players))
    print("{}: {}".format(winner + 1, score))

#main(9, 25)
#main(10, 1618)
#main(13, 7999)
#main(17, 1104)
#main(21, 6111)
#main(30, 5807)

# 412 players; last marble is worth 71646 points
main(412, 71646)
