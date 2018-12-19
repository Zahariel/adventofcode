import re

def parseInitialState(line):
    line = line[15:-1]
    return [char == "#" for char in line]

def parseRule(line):
    nbhd, result = re.match(r"(.....) => (.)", line).groups()
    nbhdNum = sum(2 ** i for (i, c) in enumerate(nbhd) if c == "#")
    return nbhdNum, (result == "#")

def safeGetValue(state, loc):
    if loc < 0 or loc >= len(state): return False
    return state[loc]

def safeGetNbhd(state, loc):
    return sum(2 ** i for i in range(5) if safeGetValue(state, loc + i - 2))

def printState(state, offset, margin):
    #print(" " * margin + "v")
    for i in range(-margin, len(state) - offset):
        if safeGetValue(state, i+offset):
            print("#", end="")
        else:
            print(".", end="")
    print()

numGenerations = 150
with open("day12input.txt") as file:
    initialState = parseInitialState(file.readline())
    file.readline()
    rules = [False for i in range(32)]
    for rule in file:
        nbhd, result = parseRule(rule)
        rules[nbhd] = result
    printState(initialState, 0, 1)

    state = initialState
    offset = 0
    for i in range(numGenerations):
        newState = [rules[safeGetNbhd(state, i)] for i in range(-2, len(state) + 2)]
        state = newState
        offset += 2
        printState(state, offset, 1)
    finalSum = sum(i - offset for (i, p) in enumerate(state) if p)
    finalCount = sum(1 for p in state if p)

print (finalSum + finalCount * (50000000000 - numGenerations))