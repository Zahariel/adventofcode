import time
puzzle_input = 5177
grid_size = 300

def calc_cell(x, y, serial):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial
    power_level *= rack_id
    return (power_level // 100) % 10 - 5

def calc_square(x, y, serial):
    return sum(calc_cell(xx, yy, serial) for xx in range(x, x+3) for yy in range(y, y+3))

start = time.perf_counter()
print(max((calc_square(x, y, puzzle_input), x, y) for x in range(1, grid_size - 1) for y in range(1, grid_size - 1)))
first = time.perf_counter()
grid = [[calc_cell(x, y, puzzle_input) for y in range(1, grid_size+1)] for x in range(1, grid_size+1)]
above_sums = [[0] for x in range(grid_size)]
left_sums = [[0 for y in range(grid_size)]]
for i in range(grid_size):
    [above_sums[x].append(above_sums[x][i] + grid[x][i]) for x in range(grid_size)]
    left_sums.append([left_sums[i][y] + grid[i][y] for y in range(grid_size)])
squares = [grid]
for size in range(2, grid_size+1):
    next_grid = [[(squares[-1][x][y] + above_sums[x+size-1][y+size-1] - above_sums[x+size-1][y] + left_sums[x+size][y+size-1] - left_sums[x][y+size-1])
                  for y in range(grid_size - size + 1)] for x in range(grid_size - size + 1)]
    squares.append(next_grid)
print(max((squares[size][x][y], x+1, y+1, size+1) for size in range(len(squares)) for x in range(grid_size - size) for y in range(grid_size - size)))
second = time.perf_counter()
print(first - start, second - first)