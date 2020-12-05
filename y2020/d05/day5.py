def parse(line):
    return [c == 'B' or c == 'R' for c in line]

with open("input.txt") as f:
    input = [parse(line.strip()) for line in f]

def seat_id(ticket):
    return sum(2**i for i, val in enumerate(reversed(ticket)) if val)

seat_ids = [seat_id(ticket) for ticket in input]
seat_ids.sort()

print(seat_ids[-1])

for idx, num in enumerate(seat_ids):
    if idx + seat_ids[0] != num:
        print(num - 1)
        break
