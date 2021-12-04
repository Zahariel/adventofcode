import functools
import operator

class Board:
    def __init__(self, rows):
        self.rows = rows
        self.marked = [[False for c in r] for r in rows]

    def mark(self, num):
        for y, r in enumerate(self.rows):
            for x, c in enumerate(r):
                if c == num:
                    self.marked[y][x] = True

    def check(self):
        # check rows
        if any(all(row) for row in self.marked): return True
        # check columns
        if any(all(row[i] for row in self.marked) for i in range(len(self.marked[0]))): return True
        # # check main diag
        # if all(self.marked[i][i] for i in range(len(self.marked))): return True
        # # check off diag
        # if all(self.marked[i][-i-1] for i in range(len(self.marked))): return True
        return False

    def score(self):
        return functools.reduce(operator.add, (num for y, r in enumerate(self.rows) for x, num in enumerate(r) if not self.marked[y][x]))

    def __str__(self):
        return "\n".join(" ".join(str(c) + ("*" if self.marked[y][x] else "") for x, c in enumerate(r)) for y, r in enumerate(self.rows))


with open("input.txt") as f:
    numbers = [int(n) for n in f.readline().strip().split(",")]
    f.readline()
    boards = []
    board = []
    for line in f.readlines():
        line = line.strip()
        if len(line) == 0:
            boards.append(Board(board))
            board = []
        else:
            board.append([int(n) for n in line.split()])
    boards.append(Board(board))

endit = False
won = 0
for num in numbers:
    for b in boards:
        if b.check(): continue
        b.mark(num)
        if b.check():
            if won == 0:
                # print the first win (part 1)
                print(num, num * b.score())
            won += 1
            if won == len(boards):
                # print the last win (part 2)
                print(num, num * b.score())
                break
    if won == len(boards): break



