from y2019.intcode import run_comp
from collections import defaultdict

with open("input.txt") as f:
    line = f.readline()

initial_cells = [int(x) for x in line.split(",")]
pixels = [' ', '#', '+', '=', '@']

class Board():
    def __init__(self):
        self.board = defaultdict(int)
        self.mode = 0
        self.score = 0
        self.x = 0
        self.y = 0
        self.scores = []
        self.paddle_x = 0
        self.ball_x = 0

    def draw(self, val):
        if self.mode == 0:
            self.x = val
            self.mode = 1
        elif self.mode == 1:
            self.y = val
            self.mode = 2
        elif self.mode == 2:
            if self.x == -1 and self.y == 0:
                self.score = val
                self.scores.append(val)
            else:
                self.board[self.x, self.y] = val
                if val == 3:
                    self.paddle_x = self.x
                elif val == 4:
                    self.ball_x = self.x
            self.mode = 0

    def draw_board(self):
        print(self.score)
        for y in range(24):
            for x in range(40):
                print(pixels[self.board[x,y]], end="")
            print()


board = Board()

run_comp(initial_cells, output_fn=board.draw)

print(sum(1 for thing in board.board.values() if thing == 2))
board.draw_board()

initial_cells[0] = 2

frames = 0
def get_input(prompt):
    global frames
    frames = frames + 1
    if frames > 10_000_000:
        board.draw_board()
        return 0
    if board.ball_x < board.paddle_x:
        return -1
    elif board.ball_x > board.paddle_x:
        return 1
    else:
        return 0

board = Board()

run_comp(initial_cells, input_fn=get_input, output_fn=board.draw)

board.draw_board()
print(board.scores)
