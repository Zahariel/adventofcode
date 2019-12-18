import itertools

with open("input.txt") as f:
    start_signal = [int(c) for c in f.readline().strip()]
    size = len(start_signal)

# precondition: idx >= start
def generate_pattern(idx, start):
    while True:
        for i in range(start + 1, idx):
            yield 0
        for i in range(idx):
            yield 1
        for i in range(idx):
            yield 0
        for i in range(idx):
            yield -1
        for i in range(start + 1):
            yield 0

# print(list(itertools.islice(generate_pattern(4, 0), 50)))

def perform_phase(signal, size, start=0):
    result = []
    for i in range(start, size):
        pattern = generate_pattern(i+1, start)
        digit = sum(a * b for a, b in zip(pattern, signal))
        result.append(abs(digit) % 10)
    return result

current_signal = start_signal
for i in range(100):
    current_signal = perform_phase(current_signal, size)

print(current_signal[:8])

# part 2
# actually calculating this is way way too expensive, but fortunately my offset is way more than length * 5000, so
# i don't have to. once the index is greater than half the length, the "pattern" just collapses to "sum every cell
# after this one", and cells before the cell in question never affect the phase.
def lazy_list_mult(l, c):
    for i in range(c):
        for v in l:
            yield v

with open("input.txt") as f:
    line = f.readline().strip()
    offset = int(line[:7])
    size = len(line) * 10000
    # we reverse it so we can use itertools.accumulate()
    signal = lazy_list_mult([int(c) for c in reversed(line)], 10000)
    # chop off the original beginning (it's not needed)
    signal = itertools.islice(signal, size - offset)

# signal = list(signal)
print(offset, size)
# print(signal[:100])

for i in range(100):
    print(i)
    signal = itertools.accumulate(signal)
    signal = map(lambda n: n % 10, signal)

print(list(reversed(list(signal)))[:8])

