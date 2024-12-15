from parsing import split_on_blank
from utils import Coord2D

MOVES = {
    "^": Coord2D(-1, 0),
    "v": Coord2D(1, 0),
    "<": Coord2D(0, -1),
    ">": Coord2D(0, 1),
}


with open("input.txt") as f:
    original_map, moves = split_on_blank(f)
    original_map = {Coord2D(r, c): cell for (r, line) in enumerate(original_map) for (c, cell) in enumerate(line)}

    moves = [MOVES[move] for move in "".join(moves)]


map = dict(original_map)

def find_robot(map):
    for loc, cell in map.items():
        if cell == "@":
            map[loc] = "."
            return loc

robot = find_robot(map)

def try_move(robot, dir):
    objective = robot + dir
    while map[objective] == "O":
        objective += dir
    if map[objective] == "#":
        return robot
    map[objective] = "O"
    map[robot + dir] = "."
    return robot + dir

for move in moves:
    robot = try_move(robot, move)

print(sum(100 * box.x + box.y for (box, contents) in map.items() if contents == "O"))


# part 2

def convert_item(item, left_side):
    if item == "O":
        return "[" if left_side else "]"
    elif item == "@":
        return "@" if left_side else "."
    else:
        return item

bigmap = {
    **{Coord2D(coord.x, coord.y * 2): convert_item(item, True) for (coord, item) in original_map.items()},
    **{Coord2D(coord.x, coord.y * 2 + 1): convert_item(item, False) for (coord, item) in original_map.items()}
}

robot = find_robot(bigmap)

def try_move2(robot, dir):
    entered_cells = {robot + dir}
    exited_cells = dict()
    while entered_cells:
        mover = entered_cells.pop()
        if mover in exited_cells: continue
        exited_cells[mover] = bigmap[mover]
        if bigmap[mover] == ".": continue
        elif bigmap[mover] == "#": return robot
        elif bigmap[mover] == "[":
            entered_cells.add(mover + dir)
            entered_cells.add(mover + Coord2D(0, 1))
        elif bigmap[mover] == "]":
            entered_cells.add(mover + dir)
            entered_cells.add(mover + Coord2D(0, -1))

    for oldloc in exited_cells.keys():
        bigmap[oldloc] = "."
    for oldloc, contents in exited_cells.items():
        if contents != ".":
            bigmap[oldloc + dir] = contents
    return robot + dir

for move in moves:
    robot = try_move2(robot, move)

print(sum(100 * box.x + box.y for (box, contents) in bigmap.items() if contents == "["))
