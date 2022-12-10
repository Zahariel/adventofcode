def parse(line):
    parts = line.split()
    if parts[0] == "noop": return None
    else: return int(parts[1])

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]

cycle = 0
x = 1
signal = 0

def check_signal():
    global signal
    if cycle % 40 == 20:
        signal += x * cycle

for inst in lines:
    if inst is None:
        cycle += 1
        check_signal()
    else:
        cycle += 1
        check_signal()
        cycle += 1
        check_signal()
        x += inst

print(signal)

# part 2
cycle = 0
x = 1
def print_pixel():
    pixel = cycle % 40
    if x-1 <= pixel <= x+1:
        print('#', end='')
    else:
        print('.', end='')
    if pixel == 39: print()

for inst in lines:
    print_pixel()
    if inst is None:
        cycle += 1
    else:
        cycle += 1
        print_pixel()
        cycle += 1
        x += inst


