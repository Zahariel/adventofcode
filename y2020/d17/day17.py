import itertools

# yep, it's 3D Game of Life

class Board:
    def __init__(self, dims):
        self.cells = set()
        self.dims = dims
        self.lower_bounds = [200] * dims
        self.upper_bounds = [-200] * dims

    def add(self, point):
        self.cells.add(point)
        self.lower_bounds = [min(val, bound) for val, bound in zip(point, self.lower_bounds)]
        self.upper_bounds = [max(val, bound) for val, bound in zip(point, self.upper_bounds)]

    def remove(self, point):
        self.cells.discard(point)

    def __getitem__(self, item):
        return item in self.cells

    def calc_neighborhood(self, point):
        return sum(1 for d_point in itertools.product(*(range(v - 1, v + 2) for v in point)) if d_point in self.cells)

    def step(self):
        new_board = Board(self.dims)
        ranges = [range(lower - 1, upper + 2) for lower, upper in zip(self.lower_bounds, self.upper_bounds)]

        for point in itertools.product(*ranges):
            neighborhood = self.calc_neighborhood(point)
            if neighborhood == 3 or (neighborhood == 4 and point in self.cells):
                new_board.add(point)

        return new_board

board = Board(3)
with open("input.txt") as f:
    for y, line in enumerate(f):
        for x, cell in enumerate(line.strip()):
            if cell == '#':
                board.add((x, y, 0))

print(board.cells)

STARTUP_LENGTH = 6
for i in range(STARTUP_LENGTH):
    board = board.step()

print(len(board.cells))

# part 2: yep, it's 4D Game of Life! time to rewrite part 1

board = Board(4)
with open("input.txt") as f:
    for y, line in enumerate(f):
        for x, cell in enumerate(line.strip()):
            if cell == '#':
                board.add((x, y, 0, 0))

for i in range(STARTUP_LENGTH):
    board = board.step()

print(len(board.cells))
