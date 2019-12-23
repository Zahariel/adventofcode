
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def moddiv(a, b, m):
    return (a * modinv(b, m)) % m

# sum 1 + r + r^2 + ... + r^n = (r^(n+1) - 1) / (r - 1)
def geometric_sum(r, n, m):
    return ((pow(r, n+1, m) - 1) * modinv(r-1, m)) % m

class Cut:
    def __init__(self, amount):
        self.amount = amount

    def perform(self, deck):
        # this works for negative amount too!
        return deck[self.amount:] + deck[:self.amount]

    def as_inc_cut(self):
        return 1, self.amount

    def __repr__(self):
        return "Cut(%d)" % self.amount

class Reverse:
    def __init__(self):
        pass

    def perform(self, deck):
        return list(reversed(deck))

    def as_inc_cut(self):
        return -1, 1

    def __repr__(self):
        return "Reverse()"

class Increment:
    def __init__(self, increment):
        self.increment = increment

    def perform(self, deck):
        result = [0] * len(deck)
        pos = 0
        for card in deck:
            result[pos] = card
            pos += self.increment
            pos %= len(deck)
        return result

    def as_inc_cut(self):
        return self.increment, 0

    def __repr__(self):
        return "Increment(%d)" % self.increment

def parse(line):
    if line.startswith("cut"):
        return Cut(int(line[4:]))
    elif line.startswith("deal with increment"):
        return Increment(int(line[20:]))
    elif line.startswith("deal into new stack"):
        return Reverse()
    else:
        print("unknown instruction", line)
        exit(1)


DECK_SIZE = 10007
with open("input.txt") as f:
    instructions = [parse(line.strip()) for line in f]

deck = [i for i in range(DECK_SIZE)]

for inst in instructions:
    deck = inst.perform(deck)

print(deck.index(2019))


DECK_SIZE = 119315717514047
ITERATIONS = 101741582076661

# flatten instructions into an Increment followed by a Cut
total_inc, total_cut = 1, 0
for inst in instructions:
    inc, cut = inst.as_inc_cut()
    total_inc, total_cut = (total_inc * inc) % DECK_SIZE, (total_cut * inc + cut) % DECK_SIZE

print("flattened", total_inc, total_cut)

final_inc = pow(total_inc, ITERATIONS, DECK_SIZE)
final_cut = (total_cut * geometric_sum(total_inc, ITERATIONS - 1, DECK_SIZE)) % DECK_SIZE

print("iterated", final_inc, final_cut)

# do the final operation backwards
print(moddiv(2020 + final_cut, final_inc, DECK_SIZE))
