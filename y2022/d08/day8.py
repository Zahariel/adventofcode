def parse(line):
    return [int(c) for c in line]

with open("input.txt") as file:
    forest = [parse(line.rstrip()) for line in file]

# part 1
visible = [[False for _ in row] for row in forest]

for r, row in enumerate(forest):
    height = -1
    for c, tree in enumerate(row):
        if tree > height:
            visible[r][c] = True
            height = tree
    height = -1
    for c, tree in reversed(list(enumerate(row))):
        if tree > height:
            visible[r][c] = True
            height = tree

for c in range(len(forest[0])):
    height = -1
    for r, row in enumerate(forest):
        if row[c] > height:
            visible[r][c] = True
            height = row[c]
    height = -1
    for r, row in reversed(list(enumerate(forest))):
        if row[c] > height:
            visible[r][c] = True
            height = row[c]

print(sum(1 for row in visible for cell in row if cell))

# part 2

def scenic_score(r, c):
    def look(dr, dc):
        height = forest[r][c]
        r2, c2 = r + dr, c + dc
        count = 0
        while r2 >= 0 and c2 >= 0 and r2 < len(forest) and c2 < len(forest[r2]):
            count += 1
            if height <= forest[r2][c2]: break
            r2 += dr
            c2 += dc
        return count

    return look(0,1) * look(1,0) * look(0,-1) * look(-1,0)

score = [[scenic_score(r, c) for c,_ in enumerate(row)] for r, row in enumerate(forest)]

print(max(max(row) for row in score))
