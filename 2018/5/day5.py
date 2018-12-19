def react(polymer):
    i = 0
    while i < len(polymer) - 1:
        left = polymer[i]
        right = polymer[i + 1]
        if left != right and left.upper() == right.upper():
            polymer[i:i+2] = []
            i = max(i - 1, 0)
        else:
            i += 1
    return polymer

def react2(polymer):
    result = []
    for right in polymer:
        if len(result) == 0:
            result.append(right)
        else:
            left = result[-1]
            if left != right and left.upper() == right.upper():
                result[-1:] = []
            else:
                result.append(right)
    return result

with open("day5input.txt") as file:
    polymer = [c for c in file.readline().strip()]
    #polymer = "dabAcCaCBAcCcaDA"
    polymer = react2(polymer)
    print(len(polymer))

    types = set(c.upper() for c in polymer)
    lens = [(len(react2([c for c in polymer if c.upper() != unit])), unit) for unit in types]
    print(min(lens))
