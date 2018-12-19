chars = [".", "|", "#"]
parse = dict((c, i) for i, c in enumerate(chars))
OPEN = parse["."]
TREES = parse["|"]
YARD = parse["#"]

def print_board(board):
    for line in board:
        for cell in line:
            print(chars[cell], end="")
        print()
    print()

def safe_get(board, x, y):
    if 0 <= y < len(board) and 0 <= x < len(board[y]): return board[y][x]
    return OPEN

def calc_square(board, x, y):
    trees, yards = 0, 0
    for yy in range(y-1, y+2):
        for xx in range(x-1, x+2):
            if x == xx and y == yy: continue
            neighbor = safe_get(board, xx, yy)
            if neighbor == TREES: trees += 1
            elif neighbor == YARD: yards += 1
    square = board[y][x]
    if square == OPEN and trees >= 3: return TREES
    if square == TREES and yards >= 3: return YARD
    if square == YARD and (trees == 0 or yards == 0): return OPEN
    return square


with open("day18input.txt") as file:
    board = tuple(tuple(parse[c] for c in line.strip()) for line in file)

cache = dict()
reverse_cache = []

#generations = 10
generations = 1000000000
i = 0
while i < generations:
    if i % 100 == 0:
        print(i)
        print_board(board)
    if board in cache:
        previous = cache[board]
        print("repeated board at", i, "from", previous)
        diff = i - previous
        victim = (generations - previous) % diff + previous
        board = reverse_cache[victim]
        break
    cache[board] = i
    reverse_cache.append(board)
    board = tuple(tuple(calc_square(board, x, y) for x, _ in enumerate(line)) for y, line in enumerate(board))
    i += 1

print(generations)
print_board(board)
trees = sum(1 for row in board for square in row if square == TREES)
yards = sum(1 for row in board for square in row if square == YARD)
print(trees, yards, trees*yards)