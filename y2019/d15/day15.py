from breadth_first import breadth_first

from y2019.intcode import CoIntComp

with open("input.txt") as f:
    line = f.readline().strip()
initial_cells = [int(cell) for cell in line.split(",")]


MOVES = [(1, 2, 0, -1), (2, 1, 0, 1), (3, 4, -1, 0), (4, 3, 1, 0)]
class Robot:
    def __init__(self):
        self.comp = CoIntComp(initial_cells)
        self.board = dict()
        self.x = 0
        self.y = 0
        self.board[0, 0] = 1

    def explore(self):
        for dir, opp, dx, dy in MOVES:
            if (self.x + dx, self.y + dy) not in self.board:
                result = self.comp.run(dir)
                self.board[self.x + dx, self.y + dy] = result
                if result != 0:
                    # keep exploring
                    self.x = self.x + dx
                    self.y = self.y + dy
                    self.explore()
                    assert self.comp.run(opp) != 0
                    self.x = self.x - dx
                    self.y = self.y - dy

    def neighbors(self, c):
        x, y = c
        return [(1, (x + dx, y + dy)) for _, _, dx, dy in MOVES if self.board[x + dx, y + dy] != 0]

    def find_oxygen(self):
        return breadth_first((0, 0), self.neighbors, lambda dist, c: (dist, c) if self.board[c[0], c[1]] == 2 else None)

    def floodfill(self, oxy_x, oxy_y):
        dists = {}

        def process(dist, c):
            dists[c] = dist
            return None

        breadth_first((oxy_x, oxy_y), self.neighbors, process)
        return max(dists.values())

    def print_board(self):
        min_x = min(x for (x, _) in self.board.keys())
        max_x = max(x for (x, _) in self.board.keys())
        min_y = min(y for (_, y) in self.board.keys())
        max_y = max(y for (_, y) in self.board.keys())
        print("*" * (max_x - min_x + 3))
        for y in range(min_y, max_y + 1):
            print("*", end="")
            for x in range(min_x, max_x + 1):
                if (x, y) not in self.board:
                    print(" ", end="")
                elif (x, y) == (self.x, self.y):
                    print("R", end="")
                elif self.board[x, y] == 0:
                    print("#", end="")
                elif self.board[x, y] == 2:
                    print("O", end="")
                else:
                    print(".", end="")
            print("*")
        print("*" * (max_x - min_x + 3))
        print()

robot = Robot()

robot.explore()

robot.print_board()

oxygen_dist, (oxygen_x, oxygen_y) = robot.find_oxygen()
print(oxygen_dist)

print(robot.floodfill(oxygen_x, oxygen_y))
