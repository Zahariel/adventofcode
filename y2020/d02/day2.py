import re
from collections import Counter

def parse(line):
    min, max, letter, password = re.match(r"(\d+)-(\d+) ([a-z]): ([a-z]+)", line).groups()
    return int(min), int(max), letter, password

with open("input.txt") as f:
    passwords = [parse(l.strip()) for l in f]

valid = 0
for min, max, letter, password in passwords:
    counter = Counter(password)
    amount = counter[letter]
    if amount >= min and amount <= max:
        valid += 1

print(valid)

valid = 0
for first, second, letter, password in passwords:
    if (password[first-1] == letter) ^ (password[second-1] == letter):
        valid += 1

print(valid)
