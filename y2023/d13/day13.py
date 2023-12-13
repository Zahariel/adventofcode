from parsing import split_on_blank

def parse(line):
    return [c == '#' for c in line]

with open("input.txt") as file:
    patterns = list(split_on_blank(file, line_parser=parse))


def look_for_horiz(pattern):
    acc = set()
    for potential in range(len(pattern) - 1):
        look_rows = min(potential + 1, len(pattern) - potential - 1)
        if all(pattern[potential - dr] == pattern[potential + dr + 1] for dr in range(look_rows)):
            acc.add(potential + 1)
    return acc

def transpose(pattern):
    return [[pattern[r][c] for r in range(len(pattern))] for c in range(len(pattern[0]))]


def find_mirrors(pattern):
    return look_for_horiz(pattern), look_for_horiz(transpose(pattern))

mirrors = [find_mirrors(pattern) for pattern in patterns]
print(sum(sum(hs) * 100 + sum(vs) for hs, vs in mirrors))


def find_smudge(pattern):
    original = find_mirrors(pattern)

    for r in range(len(pattern)):
        for c in range(len(pattern[r])):
            pattern[r][c] = not pattern[r][c]
            new_mirrors = find_mirrors(pattern)
            pattern[r][c] = not pattern[r][c]
            if new_mirrors != (set(), set()) and new_mirrors != original:
                return new_mirrors[0] - original[0], new_mirrors[1] - original[1]


new_mirrors = [find_smudge(pattern) for pattern in patterns]
print(sum(sum(hs) * 100 + sum(vs) for hs, vs in new_mirrors))
