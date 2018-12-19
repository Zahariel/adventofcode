class Node:
    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next

def calc_score(players, last_marble):
    scores = [0 for i in range(players)]
    player = 0
    current = Node(0, None, None)
    current.next = current
    current.prev = current
    for marble in range(1, last_marble+1):
        if marble % 23 == 0:
            scores[player] += marble
            for i in range(7):
                current = current.prev
            scores[player] += current.data
            current.prev.next = current.next
            current.next.prev = current.prev
            current = current.next
        else:
            current = current.next
            new_node = Node(marble, current, current.next)
            current.next.prev = new_node
            current.next = new_node
            current = new_node
        #print(player, circle)
        player = (player + 1) % players

    return max(enumerate(scores), key=lambda p: p[1])

#tests
print(calc_score(9, 25)) # 32
print(calc_score(10, 1618)) # 8317
print(calc_score(13, 7999)) # 146373
print(calc_score(17, 1104)) # 2764

#real input
print(calc_score(465, 71940))
print(calc_score(465, 7194000))