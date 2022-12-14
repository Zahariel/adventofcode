from keyeddefaultdict import KeyedDefaultdict

def parse(line):
    parts = line.split()[0::2]
    return [tuple(int(c) for c in part.split(",")) for part in parts]

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]


print(lines)

max_x = max(x for line in lines for (x, _) in line)+2
max_y = max(y for line in lines for (_, y) in line)

EMPTY = 0
SAND = 1
ROCK = 2

board = KeyedDefaultdict(lambda _: EMPTY)

def add_to_board(line):
    x, y = line[0]
    for i in range(1, len(line)):
        new_x, new_y = line[i]
        if new_x == x:
            step = 1 if y < new_y else -1
            for y2 in range(y, new_y, step):
                board[x, y2] = ROCK
            y = new_y
        else:
            step = 1 if x < new_x else -1
            for x2 in range(x, new_x, step):
                board[x2, y] = ROCK
            x = new_x
    board[x, y] = ROCK

for line in lines:
    add_to_board(line)

def drop_sand():
    x, y = 500, 0
    while True:
        if y >= max_y+3:
            return False
        if board[x, y+1] == EMPTY:
            y += 1
        elif board[x-1, y+1] == EMPTY:
            x, y = x-1, y+1
        elif board[x+1, y+1] == EMPTY:
            x, y = x+1, y+1
        else:
            board[x, y] = SAND
            return True

stopped = True
count = 0
while stopped:
    count += 1
    stopped = drop_sand()

print(count-1)

# part 2

board = KeyedDefaultdict(lambda p: ROCK if p[1] == max_y+2 else EMPTY)
for line in lines:
    add_to_board(line)

count = 0
stopped = True
while stopped and board[500, 0] == EMPTY:
    count += 1
    stopped = drop_sand()

print(count)
