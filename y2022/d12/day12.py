from breadth_first import ortho_neighbors, breadth_first

def parse_letter(letter):
    if letter == 'S': return 0, True, False
    if letter == 'E': return 25, False, True
    return ord(letter) - ord('a'), False, False

def parse(line):
    return [parse_letter(letter) for letter in line]

with open("input.txt") as file:
    height_map = [parse(line.rstrip()) for line in file]

HEIGHT = len(height_map)
WIDTH = len(height_map[0])

def neighbors(loc):
    r, c = loc
    height, _, _ = height_map[r][c]
    for _, (r2, c2) in ortho_neighbors((0, HEIGHT), (0, WIDTH))(loc):
        if height_map[r2][c2][0] <= height + 1:
            yield 1, (r2, c2)

start_r, start_c = 0, 0
end_r, end_c = 0, 0

for r, row in enumerate(height_map):
    for c, col in enumerate(row):
        if height_map[r][c][1]:
            start_r, start_c = r, c
        if height_map[r][c][2]:
            end_r, end_c = r, c

def check(dist, loc):
    r, c = loc
    if r == end_r and c == end_c:
        return dist


distance = breadth_first((start_r, start_c), neighbors_fn=neighbors, process_fn=check)

print(distance)


# part 2
# do it backwards

def neighbors2(loc):
    r, c = loc
    height, _, _ = height_map[r][c]
    for _, (r2, c2) in ortho_neighbors((0, HEIGHT), (0, WIDTH))(loc):
        if height_map[r2][c2][0] >= height - 1:
            yield 1, (r2, c2)

def check2(dist, loc):
    r, c = loc
    if height_map[r][c][0] == 0:
        return dist

distance = breadth_first((end_r, end_c), neighbors_fn=neighbors2, process_fn=check2)
print(distance)
