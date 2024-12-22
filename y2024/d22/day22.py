import itertools
from collections import Counter

from collection_utils import n_wise


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
    for history in n_wise(price_list, 5):
        diffs = tuple(b - a for a, b in itertools.pairwise(history))
        if diffs not in answer:
            answer[diffs] = history[-1]
    return answer

final_results = Counter()
for prices in all_prices:
    final_results.update(construct_results(prices))

print(max(final_results.values()))
