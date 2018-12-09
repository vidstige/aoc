from typing import Any

class Node(object):
    def __init__(self, left, right, value: Any):
        self.left = left or self
        self.right = right or self
        self.value = value

class circular(object):
    def __init__(self):
        self.first = None

    def insert(self, value: Any) -> None:
        if self.first is None:
            self.first = Node(None, None, value)
        else:
            first = self.first
            node = Node(first.left, first, value)
            first.left.right = node
            first.left = node
            self.first = node

    def pop(self, at=0) -> Any:
        node = self.first
        for _ in range(at):
            node = node.right
        
        left = node.left
        right = node.right
        
        left.right = right
        right.left = left

        # was first unlinked?
        if self.first == node:
            self.first = right

        return node.value

    def rotate(self, n) -> None:
        """rotates the list n steps"""
        node = self.first
        if node is None:
            return

        for _ in range(abs(n)):
            node = node.right if n > 0 else node.left
        self.first = node

    def __iter__(self):
        node = self.first
        if node is not None:
            yield node.value
            node = node.right
            while node != self.first:
                yield node.value
                node = node.right                

def circle(raw, items):
    return raw % len(items)

def main(player_count, marble_count):
    marbles = circular()
    marbles.insert(0)
    #index = None
    players = [0] * player_count
    for m in range(1, marble_count + 1):
        player = circle(m - 1, players)

        if m % 23 == 0:
            players[player] += m
            marbles.rotate(-7)
            players[player] += marbles.pop()
        else:
            marbles.rotate(2)
            marbles.insert(m)
        #print(player, list(marbles))
    score, winner = max((s, i) for i, s in enumerate(players))
    print("{}: {}".format(winner + 1, score))

main(9, 25)
#main(10, 1618)
#main(13, 7999)
#main(17, 1104)
#main(21, 6111)
#main(30, 5807)

# 412 players; last marble is worth 71646 points
main(412, 7164600)
