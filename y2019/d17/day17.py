from y2019.intcode import IntComp, InputFunction

with open("input.txt") as f:
    line = f.readline().strip()
    initial_cells = [int(n) for n in line.split(",")]

image = []
current_row = ""

def get_pixel(pixel):
    global image, current_row
    if pixel == 10:
        image.append(current_row)
        current_row = ""
    else:
        current_row = current_row + (chr(pixel))

comp = IntComp(initial_cells, output_fn=get_pixel)

comp.run()

# i'm getting an extra blank row at the end, hooray for underspecified output formats
image = image[:-1]

for y, row in enumerate(image):
    print(str(y).center(2), row)

acc = 0
for y, row in enumerate(image):
    if y == 0 or y == len(image) - 1:
        continue
    for x, pixel in enumerate(row):
        if x == 0 or x == len(row) - 1:
            continue
        if pixel != '#':
            continue
        if image[y-1][x] == '#' and image[y+1][x] == '#' and image[y][x-1] == '#' and image[y][x+1] == '#':
            acc = acc + x * y

print(acc)


# the dream:
# R,6,L,12,R,6, R,6,L,12,R,6, L,12,R,6,L,8,L,12, R,12,L,10,L,10, L,12,R,6,L,8,L,12, R,12,L,10,L,10, L,12,R,6,L,8,L,12, R,12,L,10,L,10, L,12,R,6,L,8,L,12, R,6,L,12,R,6
#
#   01234567890123456789
# M A,A,B,C,B,C,B,C,B,A
# A R,6,L,12,R,6
# B L,12,R,6,L,8,L,12
# C R,12,L,10,L,10

M = "A,A,B,C,B,C,B,C,B,A"
A = "R,6,L,12,R,6"
B = "L,12,R,6,L,8,L,12"
C = "R,12,L,10,L,10"

def listify(string):
    result = [ord(c) for c in string]
    result.append(10)
    return result

inputs = listify(M) + listify(A) + listify(B) + listify(C) + listify("n")

initial_cells[0] = 2
new_comp = IntComp(initial_cells, output_fn=lambda c: print(c) if c > 255 else print(chr(c), end=""), input_fn=InputFunction(inputs))
new_comp.run()

