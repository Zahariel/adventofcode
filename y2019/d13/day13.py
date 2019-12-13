from y2019.intcode import run_comp, FrameOutput
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

    def frame_draw(self, x, y, val):
        if x == -1 and y == 0:
            self.score = val
            self.scores.append(val)
        else:
            self.board[x, y] = val
            if val == 3:
                self.paddle_x = x
            elif val == 4:
                self.ball_x = x

    def draw_board(self):
        print(self.score)
        for y in range(24):
            for x in range(40):
                print(pixels[self.board[x,y]], end="")
            print()


board = Board()

run_comp(initial_cells, output_fn=FrameOutput(3, board.frame_draw))

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

run_comp(initial_cells, input_fn=get_input, output_fn=FrameOutput(3,board.frame_draw))

board.draw_board()
print(board.scores)
