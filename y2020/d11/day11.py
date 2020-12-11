
FILE = "input.txt"
with open(FILE) as f:
    seats = [list(line.strip()) for line in f]

FLOOR = '.'
EMPTY = 'L'
OCCUPIED = '#'

def nearby(row, col, seats):
    top = max(row-1, 0)
    bottom = min(row+2, len(seats))
    left = max(col-1, 0)
    right = min(col+2, len(seats[0]))
    return sum(1 for row in seats[top:bottom] for seat in row[left:right] if seat == OCCUPIED)

# given rules:
# empty seat becomes occupied if it has 0 occupied neighbors
# occupied seat becomes empty if it has at least 4 occupied neighbors
# equivalent formation (including a seat as "nearby" itself):
# any seat becomes occupied if it has 0 occupied seats nearby
# any seat becomes empty if it has at least threshold occupied seats nearby
# otherwise it doesn't change

def step(row, col, seats, threshold, counter=nearby):
    current = seats[row][col]
    if current == FLOOR:
        return FLOOR
    count = counter(row, col, seats)
    if count == 0:
        return OCCUPIED
    if count >= threshold:
        return EMPTY
    return current

changes = True
while changes:
    new_seats = [[step(row, col, seats, 5) for col in range(len(seat_row))] for row, seat_row in enumerate(seats)]
    changes = 0 != sum(1 for row in range(len(seats)) for col in range(len(seats[0])) if seats[row][col] != new_seats[row][col])
    seats = new_seats

print(sum(1 for row in seats for seat in row if seat == OCCUPIED))

# part 2
with open(FILE) as f:
    seats = [list(line.strip()) for line in f]

def visible_one(row, col, dr, dc, seats):
    # starting location doesn't count now
    row += dr
    col += dc
    while row >= 0 and row < len(seats) and col >= 0 and col < len(seats[row]):
        if seats[row][col] != FLOOR:
            return seats[row][col]
        row += dr
        col += dc
    return FLOOR

DIRS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
def visible(row, col, seats):
    return sum(1 for dr, dc in DIRS if visible_one(row, col, dr, dc, seats) == OCCUPIED)

def print_seats(seats):
    for row in seats:
        print("".join(row))
    print()

#print_seats(seats)
changes = True
while changes:
    new_seats = [[step(row, col, seats, 5, visible) for col in range(len(seat_row)) ] for row, seat_row in enumerate(seats)]
    changes = 0 != sum(1 for row in range(len(seats)) for col in range(len(seats[0])) if seats[row][col] != new_seats[row][col])
    seats = new_seats
    #print_seats(seats)

print(sum(1 for row in seats for seat in row if seat == OCCUPIED))
