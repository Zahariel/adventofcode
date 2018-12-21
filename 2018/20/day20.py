
def print_expr(expr, pos):
    print(" " * pos + "v")
    print(expr)

moves = {"W": (-1, 0), "E": (1, 0), "N": (0, -1), "S": (0, 1)}

def parse(expr, pos, distances, start_x, start_y):
    x, y, length = start_x, start_y, distances[(start_x, start_y)]
    while expr[pos] != "$" and expr[pos] != ")":
        print_expr(expr, pos)
        print(x, y, length)
        move = expr[pos]
        if move == "(":
            pos = parse(expr, pos+1, distances, x, y)
            # can ignore displacement caused by subexpressions
        elif move == "|":
            x, y, length = start_x, start_y, distances[(start_x, start_y)]
        else:
            dx, dy = moves[move]
            x += dx
            y += dy
            if (x, y) in distances:
                length = distances[(x, y)]
            else:
                length += 1
                distances[(x, y)] = length
        pos += 1
    print_expr(expr, pos)
    return pos


with open("day20test5.txt") as file:
    expr = file.readline().strip()

start_x, start_y = 200, 200
distances = {(start_x, start_y): 0}
pos = parse(expr, 1, distances, start_x, start_y)
if pos != len(expr) - 1:
    print("didn't reach end", pos, len(expr))

print(max(distances.values()))
print(sum(1 for range in distances.values() if range >= 1000))