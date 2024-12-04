from utils import in_bounds, coord_vector, DIAG_DIRS, ORTHO_DIRS

with open("input.txt") as f:
    lines = [line.rstrip() for line in f]

TARGET = "XMAS"

def safe_check(needle, coords):
    if needle == " ": return True # we don't care about spaces
    row, col = coords
    if not in_bounds(lines, row, col): return False
    return lines[row][col] == needle

def check_for_target(target, row, col, dir_pair):
    rdir, cdir = dir_pair
    return all(safe_check(c, loc) for trow, row_start in zip(target, coord_vector((row, col), rdir)) for c, loc in zip(trow, coord_vector(row_start, cdir)))

DIRS = ORTHO_DIRS + DIAG_DIRS
print(sum(1 for r, line in enumerate(lines) for c in range(len(line)) for dir in DIRS if check_for_target([TARGET], r, c, (None, dir))))

TARGET2 = [
    "M S",
    " A ",
    "M S",
]
DIRS2 = list(zip(ORTHO_DIRS, ORTHO_DIRS[-1:] + ORTHO_DIRS[:-1]))

print(sum(1 for r, line in enumerate(lines) for c in range(len(line)) for dir_pair in DIRS2 if check_for_target(TARGET2, r, c, dir_pair)))
