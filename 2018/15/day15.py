import heapq

class Square:
    def __init__(self, team, hp):
        self.team = team
        self.hp = hp

    def __repr__(self):
        return "Square(%d, %d)" % (self.team, self.hp)

    def get_damage(self, elf_damage):
        return 3

class Empty(Square):
    def __init__(self):
        super().__init__(-2, 0)

class Wall(Square):
    def __init__(self):
        super().__init__(-1, 0)

class Elf(Square):
    def __init__(self):
        super().__init__(0, 200)

    def get_damage(self, elf_damage):
        return elf_damage

class Goblin(Square):
    def __init__(self):
        super().__init__(1, 200)


EMPTY = Empty()
WALL = Wall()

cells = [".", "#", "E", "G"]
def print_cell(c):
    print(cells[c.team + 2], end="")

def print_grid(grid):
    print("   ", end = "")
    for i in range(len(grid[0])):
        if i % 10 == 0: print(i // 10, end="")
        elif i % 10 == 5: print(".", end="")
        else: print(" ", end="")
    print()
    for i, line in enumerate(grid):
        print("%2d" % i, end=" ")
        for cell in line:
            print_cell(cell)
        print(end="  ")
        for cell in line:
            if cell.team >= 0:
                print(cell.hp, end=" ")
        print()


def parse_cell(c):
    if c == "#": return WALL
    if c == ".": return EMPTY
    if c == "E": return Elf()
    if c == "G": return Goblin()
    print("Unexpected cell", c)
    return EMPTY

def neighbors(x, y):
    # make sure to add these in order
    yield x, y-1
    yield x-1, y
    yield x+1, y
    yield x, y+1

def is_target_space(grid, x, y, team):
    return any(grid[yy][xx].team == 1 - team for xx, yy in neighbors(x, y))

def safe_get(grid, x, y):
    if y < 0 or y >= len(grid): return EMPTY
    if x < 0 or x >= len(grid[y]): return EMPTY
    return grid[y][x]

def get_step(grid, x, y):
    team = grid[y][x].team
    if is_target_space(grid, x, y, team): return x, y
    seen = set()
    # queue has distance, current y, current x, first step y, first step x
    # never put non-empty squares in the queue
    queue = []
    for xx, yy in neighbors(x, y):
        if safe_get(grid, xx, yy) == EMPTY:
            heapq.heappush(queue, (1, yy, xx, yy, xx))
    while len(queue) > 0:
        dist, yy, xx, fy, fx = heapq.heappop(queue)
        if (xx, yy) in seen: continue
        seen.add((xx, yy))
        if is_target_space(grid, xx, yy, team):
            return fx, fy
        for nx, ny in neighbors(xx, yy):
            if safe_get(grid, nx, ny) == EMPTY and (nx, ny) not in seen:
                heapq.heappush(queue, (dist + 1, ny, nx, fy, fx))
    return x, y

def get_victim(grid, x, y):
    team = grid[y][x].team
    victims = []
    for tx, ty in neighbors(x, y):
        victim = safe_get(grid, tx, ty)
        if victim.team == 1 - team:
            victims.append((victim.hp, ty, tx, victim.team))
    if len(victims) == 0:
        return -1, -1, -1, -1
    return min(victims)

def harm_victim(grid, x, y, amount):
    victim = grid[y][x]
    victim.hp -= amount

def fight(grid, elf_damage):
    round = 0
    teams = [sum(1 for line in grid for cell in line if cell.team == team) for team in range(2)]
    while all(teams):
        new_grid = [[cell for cell in row] for row in grid]
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell.team < 0: continue
                if not all(teams):
                    return round, new_grid, False
                xx, yy = get_step(new_grid, x, y)
                new_grid[y][x] = EMPTY
                new_grid[yy][xx] = cell

                hp, ty, tx, team = get_victim(new_grid, xx, yy)
                if hp > 0:
                    #print("attack at ", tx, ty, new_grid[ty][tx], " -> ", end="")
                    harm_victim(new_grid, tx, ty, cell.get_damage(elf_damage))
                    #print(new_grid[ty][tx])
                    if new_grid[ty][tx].hp <= 0:
                        new_grid[ty][tx] = EMPTY
                        teams[team] -= 1
                        if team == 0:
                            # elf died, abort!
                            return round, new_grid, True
                        # delete from old grid so dead guy doesn't get a turn
                        grid[ty][tx] = EMPTY
        grid = new_grid
        round += 1
    return round, grid, False

elf_death = True
elf_power = 3
while elf_death:
    elf_power += 1
    #with open("openday15test1.txt") as file: # 47 * 590 = 27730
    #with open("day15test2.txt") as file: # 37 * 982 = 36334
    #with open("day15test3.txt") as file: # 46 * 859 = 39514
    #with open("day15test4.txt") as file: # 35 * 793 = 27755
    #with open("day15test5.txt") as file: # 54 * 536 = 28944
    #with open("day15test6.txt") as file: # 20 * 937 = 18740
    #with open("day15unit4.txt") as file:
    with open("day15input.txt") as file:
        grid = [[parse_cell(c) for c in line.strip()] for line in file]
    rounds, grid, elf_death = fight(grid, elf_power)
    print_grid(grid)
    hps = sum(square.hp for row in grid for square in row)
    print(elf_power, rounds, hps, rounds * hps)