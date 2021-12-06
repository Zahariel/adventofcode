
with open("input.txt") as f:
    line = f.readline()
    fishes = [int(n) for n in line.strip().split(",")]

ocean = [0] * 9

for f in fishes:
    ocean[f] += 1

def do_gen(ocean):
    spawning = ocean[0]
    ocean = ocean[1:] + [0]
    ocean[6] += spawning
    ocean[8] += spawning
    return ocean

print(ocean)

GENERATIONS = 80

for i in range(GENERATIONS):
    ocean = do_gen(ocean)
    # print(i, ocean)

print(sum(ocean))

GENERATIONS = 256 - 80
for i in range(GENERATIONS):
    ocean = do_gen(ocean)
    # print(i, ocean)

print(sum(ocean))



