import re

class Vent:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

        if self.x1 > self.x2 or (self.x1 == self.x2 and self.y1 > self.y2):
            self.x1, self.y1, self.x2, self.y2 = self.x2, self.y2, self.x1, self.y1

    def is_ortho(self):
        return self.x1 == self.x2 or self.y1 == self.y2

    def draw(self, grid):
        if self.x1 == self.x2:
            for i in range(self.y1, self.y2 + 1):
                grid[i][self.x1] += 1
        else:
            step = 0 if self.y1 == self.y2 else 1 if self.y1 < self.y2 else -1
            for i in range(self.x2 - self.x1 + 1):
                grid[self.y1 + step * i][self.x1 + i] += 1

    def __str__(self):
        return f"{self.x1},{self.y1} -> {self.x2},{self.y2}"

def parse(line):
    x1, y1, x2, y2 = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line.strip()).groups()
    return Vent(x1, y1, x2, y2)

with open("input.txt") as f:
    lines = f.readlines()
    data = [parse(line) for line in lines]

SIZE = 1000
ortho_grid = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
grid = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

for v in data:
    v.draw(grid)
    if v.is_ortho():
        v.draw(ortho_grid)

print(sum(1 if c > 1 else 0 for r in ortho_grid for c in r))
print(sum(1 if c > 1 else 0 for r in grid for c in r))
