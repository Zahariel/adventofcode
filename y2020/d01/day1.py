import itertools

with open("input.txt") as f:
    numbers = [int(n.strip()) for n in f]

numset = set()
for n in numbers:
    if (2020 - n) in numset:
        print(n * (2020 - n))
        break
    numset.add(n)

numset = set(numbers)

for n, m in itertools.combinations(numset, 2):
    if (2020 - n - m) in numset:
        print (n * m * (2020 - n - m))
        break


