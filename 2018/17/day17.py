import re

# states
DRY = 0
CLAY = 1
FLOODED = 2
DAMP = 3

chars = [".", "#", "~", "|"]
def print_board(board, left, right):
    print("    ", end="")
    for x in range(left, right):
        print(x // 100, end="")
    print()
    print("    ", end="")
    for x in range(left, right):
        print(x // 10 % 10, end="")
    print()
    print("    ", end="")
    for x in range(left, right):
        print(x % 10, end="")
    print()
    for y, line in enumerate(board):
        print("%3d" % y, end=" ")
        for state in line[left:right]:
            print(chars[state], end="")
        print()

def in_bounds(board, x, y):
    return 0 <= y < len(board) and 0 <= x < len(board[y])
def safe_get(board, x, y):
    if not in_bounds(board, x, y): return DAMP
    return board[y][x]

# returns x1, x2, y1, y2 as closed intervals
def parse_line(line):
    dir, p, q1, q2 = re.match(r"(.)=(\d+), .=(\d+)\.\.(\d+)", line).groups()
    if dir == "x":
        return int(p), int(p), int(q1), int(q2)
    else:
        return int(q1), int(q2), int(p), int(p)

with open("day17input.txt") as file:
    seams = [parse_line(line) for line in file]
x_min = min(x1 for (x1, _, _, _) in seams)
x_max = max(x2 for (_, x2, _, _) in seams)
y_min = min(y1 for (_, _, y1, _) in seams)
y_max = max(y2 for (_, _, _, y2) in seams)
board = [[DRY for _ in range(x_max + 2)] for _ in range(y_max + 1)]
for x1, x2, y1, y2 in seams:
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            board[y][x] = CLAY
print_board(board, x_min - 1, x_max + 2)

def deflood(x, y, dir):
    while board[y][x] == FLOODED:
        board[y][x] = DAMP
        x += dir

def process(startx, starty):
    stack = [(startx, starty, 0)]
    while len(stack) > 0:
        x, y, dir = stack[-1]
        if board[y][x] != DRY:
            # already processed
            stack.pop()
            continue
        below = safe_get(board, x, y+1)
        if below == DAMP:
            board[y][x] = DAMP
            stack.pop()
        elif below == DRY:
            stack.append((x, y+1, 0))
        else:
            # otherwise below is blocked, check sides
            if dir != 0:
                side = safe_get(board, x+dir, y)
                if side == DAMP:
                    board[y][x] = DAMP
                    stack.pop()
                elif side == DRY:
                    stack.append((x+dir, y, dir))
                else:
                    board[y][x] = FLOODED
                    stack.pop()
            else:
                left = safe_get(board, x-1, y)
                if left == DRY:
                    stack.append((x-1, y, -1))
                    continue
                right = safe_get(board, x+1, y)
                if right == DRY:
                    stack.append((x+1, y, 1))
                    continue
                if left != DAMP and right != DAMP:
                    board[y][x] = FLOODED
                    stack.pop()
                else:
                    deflood(x-1, y, -1)
                    deflood(x+1, y, 1)
                    board[y][x] = DAMP
                    stack.pop()

process(500, 0)
print_board(board, x_min - 1, x_max + 2)
print(sum(1 for row in board[y_min:] for cell in row if cell == DAMP or cell == FLOODED))
print(sum(1 for row in board for cell in row if cell == FLOODED))