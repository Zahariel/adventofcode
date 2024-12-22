import itertools
from collections import Counter


def parse(line):
    return int(line)


with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

def prune(secret):
    return secret & 16777215

def evolve(secret):
    secret = prune(secret ^ (secret << 6))
    secret = prune(secret ^ (secret >> 5))
    secret = prune(secret ^ (secret << 11))
    return secret

def full_evolve(secret, cycles):
    for i in range(cycles):
        secret = evolve(secret)
    return secret

print(sum(full_evolve(secret, 2000) for secret in lines))

# part 2

def calc_prices(secret):
    def iterator(secret):
        yield secret % 10
        for i in range(2000):
            secret = evolve(secret)
            yield secret % 10
    return list(iterator(secret))

all_prices = [calc_prices(secret) for secret in lines]

def construct_results(price_list):
    answer = Counter()
    history = []
    for last, current in itertools.pairwise(price_list):
        if len(history) == 4:
            history.pop(0)
        history.append(current - last)
        if len(history) == 4 and tuple(history) not in answer:
            answer[tuple(history)] = current
    return answer

final_results = Counter()
for prices in all_prices:
    final_results.update(construct_results(prices))

print(max(final_results.values()))
