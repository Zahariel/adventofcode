from y2019.intcode import IntComp
from collections import defaultdict

with open("input.txt") as f:
    line = f.readline()

initial_cells = [int(x) for x in line.split(",")]

class Robot():
    def __init__(self):
        self.board = defaultdict(int)
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = -1
        self.moving = False
        self.painted = set()

    def read(self, prompt):
        return self.board[self.x, self.y]

    def process(self, val):
        if self.moving:
            if val == 0:
                # turn left
                self.dx, self.dy = self.dy, -self.dx
            else:
                # turn right
                self.dx, self.dy = -self.dy, self.dx
            # move
            self.x = self.x + self.dx
            self.y = self.y + self.dy
            self.moving = False
        else:
            self.board[self.x, self.y] = val
            self.painted.add((self.x, self.y))
            self.moving = True


robot = Robot()
comp = IntComp(initial_cells, input_fn=robot.read, output_fn=robot.process)
comp.run()
print(len(robot.painted))

robot = Robot()
# start on white
robot.board[0,0] = 1
comp = IntComp(initial_cells, input_fn=robot.read, output_fn=robot.process)
comp.run()

min_x = min(x for (x, _) in robot.board.keys())
max_x = max(x for (x, _) in robot.board.keys())
min_y = min(y for (_, y) in robot.board.keys())
max_y = max(y for (_, y) in robot.board.keys())

for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        if robot.board[x, y] == 1:
            print("#", end="")
        else:
            print(".", end="")
    print()

