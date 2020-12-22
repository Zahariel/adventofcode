from collections import deque

class Deck:
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = deque(cards)

    def add_card(self, card):
        self.cards.append(card)

    def has_cards(self):
        return len(self.cards) > 0

    def __len__(self):
        return len(self.cards)

    def copy_cards(self, amt):
        result = [self.draw_card() for i in range(amt)]
        [self.cards.appendleft(card) for card in reversed(result)]
        return result

    def __repr__(self):
        return f"Deck({self.cards})"

    def draw_card(self):
        return self.cards.popleft()

    def score(self):
        return sum(card * val for card, val in zip(self.cards, range(len(self.cards), 0, -1)))


def read_input():
    with open("input.txt") as f:
        # player 1
        f.readline()
        player_1 = Deck()
        for line in f:
            line = line.strip()
            if len(line) == 0:
                break
            player_1.add_card(int(line))

        # player 2
        f.readline()
        player_2 = Deck()
        for line in f:
            line = line.strip()
            player_2.add_card(int(line))
    return player_1, player_2

# part 1
player_1, player_2 = read_input()

# play the game
while player_1.has_cards() and player_2.has_cards():
    card_1 = player_1.draw_card()
    card_2 = player_2.draw_card()
    if card_1 > card_2:
        player_1.add_card(card_1)
        player_1.add_card(card_2)
    else:
        player_2.add_card(card_2)
        player_2.add_card(card_1)

if player_1.has_cards():
    print("P1:", player_1.score())
else:
    print("P2:", player_2.score())


# part 2
def recursive_combat(player_1: Deck, player_2: Deck):
    cache = set()
    while player_1.has_cards() and player_2.has_cards():
        if (tuple(player_1.cards), tuple(player_2.cards)) in cache:
            return True, player_1.score()
        cache.add((tuple(player_1.cards), tuple(player_2.cards)))
        card_1 = player_1.draw_card()
        card_2 = player_2.draw_card()
        if card_1 > len(player_1) or card_2 > len(player_2):
            player_1_wins = (card_1 > card_2)
        else:
            player_1_wins, _ = recursive_combat(Deck(player_1.copy_cards(card_1)), Deck(player_2.copy_cards(card_2)))

        if player_1_wins:
            player_1.add_card(card_1)
            player_1.add_card(card_2)
        else:
            player_2.add_card(card_2)
            player_2.add_card(card_1)
    if player_1.has_cards():
        return True, player_1.score()
    else:
        return False, player_2.score()


player_1, player_2 = read_input()
print(recursive_combat(player_1, player_2))
