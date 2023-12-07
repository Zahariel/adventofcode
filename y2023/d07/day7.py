from collections import Counter

from parsy import regex, seq, whitespace

from parsing import number

RANKS = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
}

def translate_cards(hand):
    return [RANKS.get(card, int(card)) for card in hand]

def parse(line):
    parser = seq(
        regex(r"[\dAKQJT]{5}").map(translate_cards) << whitespace,
        number
    ).map(tuple)
    return parser.parse(line)

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]


def rank_hand(hand):
    counter = Counter(hand)
    frequencies = list(sorted(counter.values()))
    return rank_frequencies(frequencies)

def rank_frequencies(frequencies):
    if frequencies == [5]:
        # five of a kind
        return 7
    if frequencies == [1, 4]:
        # four of a kind
        return 6
    if frequencies == [2, 3]:
        # full house
        return 5
    if frequencies == [1, 1, 3]:
        # trips
        return 4
    if frequencies == [1, 2, 2]:
        # two pair
        return 3
    if frequencies == [1, 1, 1, 2]:
        # pair
        return 2
    # high card
    return 1

sorted_hands = sorted(lines, key=lambda h: (rank_hand(h[0]), *h[0]))

print(sum((i+1)*bid for i, (_, bid) in enumerate(sorted_hands)))


# part 2

wild_hands = [([1 if card == 11 else card for card in hand], bid) for hand, bid in lines]

def rank_hand_jokers(hand:list[int]):
    counter = Counter(hand)
    jokers = counter[1] or 0
    del counter[1]
    frequencies = list(sorted(counter.values()))
    if not frequencies: return 7

    frequencies[-1] += jokers
    return rank_frequencies(frequencies)

sorted_hands_jokers = sorted(wild_hands, key=lambda h: (rank_hand_jokers(h[0]), *h[0]))
print(sum((i+1) * bid for (i, (_, bid)) in enumerate(sorted_hands_jokers)))

