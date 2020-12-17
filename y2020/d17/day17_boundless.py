from collections import defaultdict
from itertools import product

class Board:
    def __init__(self):
        self.cells = set()

    def add(self, point):
        self.cells.add(point)

    def step(self):
        neighborhoods = defaultdict(int)

        for point in self.cells:
            for d_point in product(*(range(v-1, v+2) for v in point)):
                neighborhoods[d_point] += 1

        new_board = Board()
        for d_point, neighbors in neighborhoods.items():
            if neighbors == 3 or (neighbors == 4 and d_point in self.cells):
                new_board.add(d_point)
        return new_board


STARTUP_LENGTH = 6

board = Board()
with open("input.txt") as f:
    for y, line in enumerate(f):
        for x, cell in enumerate(line.strip()):
            if cell == '#':
                board.add((x, y, 0))

for i in range(STARTUP_LENGTH):
    board = board.step()

print(len(board.cells))

board = Board()
with open("input.txt") as f:
    for y, line in enumerate(f):
        for x, cell in enumerate(line.strip()):
            if cell == '#':
                board.add((x, y, 0, 0))

for i in range(STARTUP_LENGTH):
    board = board.step()

print(len(board.cells))
