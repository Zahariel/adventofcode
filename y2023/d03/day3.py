from coord_utils import in_bounds

def parse(line):
    return [c for c in line]

with open("input.txt") as file:
    lines: list[list[str]] = [parse(line.rstrip()) for line in file]

def is_symbol(r, c):
    return in_bounds(lines, r, c) and lines[r][c] != '.' and not lines[r][c].isdigit()

def is_digit(r, c):
    return in_bounds(lines, r, c) and lines[r][c].isdigit()

def adj_symbol(r, c):
    return any(is_symbol(r2, c2) for r2 in [r-1, r, r+1] for c2 in [c-1, c, c+1])

def find_adj_symbol(r, c):
    while is_digit(r, c):
        if adj_symbol(r, c): return True
        c += 1
    return False

def read_part_number(r, c):
    answer = 0
    while is_digit(r, c):
        answer *= 10
        answer += int(lines[r][c])
        c += 1
    return answer

def is_part_number(r, c):
    if not is_digit(r, c): return 0
    if is_digit(r, c-1): return 0
    if not find_adj_symbol(r, c): return 0
    return read_part_number(r, c)

print(sum(is_part_number(r, c) for r, line in enumerate(lines) for c in range(len(line))))


def read_any_part_number(r, c):
    if not is_digit(r, c): return None
    while is_digit(r, c-1):
        c -= 1
    return read_part_number(r, c), r, c

def is_gear(r, c):
    if lines[r][c] != '*': return 0
    numbers = list({read_any_part_number(r2, c2) for r2 in [r-1, r, r+1] for c2 in [c-1, c, c+1]})
    numbers.remove(None)
    if len(numbers) != 2: return 0
    return numbers[0][0] * numbers[1][0]


print(sum(is_gear(r, c) for r, line in enumerate(lines) for c in range(len(line))))
