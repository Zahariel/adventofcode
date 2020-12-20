import itertools

import typing

class Tile:
    def __init__(self, tile_num, rows):
        self.tile_num = tile_num
        self.pixels = [[ch == '#' for ch in row] for row in rows]
        self.edges = [
            self.pixels[0],
            [row[-1] for row in self.pixels],
            list(reversed(self.pixels[-1])),
            list(reversed([row[0] for row in self.pixels])),
        ]

    def __str__(self):
        return "\n".join("".join("#" if pixel else "." for pixel in row) for row in self.pixels)

class LayoutTile:
    def __init__(self, tile, orientation, rev):
        self.tile = tile
        self.orientation = orientation
        self.rev = rev
        self.edges = [self._edge(i) for i in range(4)]
        self.reversed_edges = [list(reversed(edge)) for edge in self.edges]

    def _edge(self, side):
        if self.rev:
            side = -side
        edge = self.tile.edges[(self.orientation + side) % 4]
        if self.rev:
            return list(reversed(edge))
        else:
            return edge

    def pixel(self, d_row, d_col):
        # skip the edges
        d_row += 1
        d_col += 1
        # reverse if necessary
        if self.rev:
            d_col = 9 - d_col
        # rotate to the right orientation
        for i in range(self.orientation):
            d_row, d_col = d_col, 9 - d_row
        return self.tile.pixels[d_row][d_col]

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

ALL_ORIENTATIONS = list(itertools.product([NORTH, EAST, SOUTH, WEST], [True, False]))

def attempt_layout(layout, row, col, used):
    if row >= len(layout):
        return layout
    to_north = layout[row-1][col].reversed_edges[SOUTH] if row != 0 else None
    to_west = layout[row][col-1].reversed_edges[EAST] if col != 0 else None

    for tile_num, tile in tiles.items():
        if tile_num in used:
            # print(f"{tile_num} already used")
            continue
        for orientation, rev in ALL_ORIENTATIONS:
            # print(f"trying {tile_num} {orientation} {rev} at {row} {col} ({used})")
            layout_tile = LayoutTile(tile, orientation, rev)
            # check north edge
            if row != 0 and layout_tile.edges[NORTH] != to_north:
                # print(f"N: {layout_tile.edges[NORTH]} != {to_north}")
                continue
            # check west edge
            if col != 0 and layout_tile.edges[WEST] != to_west:
                # print(f"W: {layout_tile.edges[WEST]} != {to_west}")
                continue

            # tile fits; attempt to continue layout
            layout[row][col] = layout_tile
            used.add(tile_num)
            next_col = (col + 1) % len(layout[row])
            next_row = row if next_col > 0 else row + 1
            result = attempt_layout(layout, next_row, next_col, used)
            if result:
                return result
            # otherwise try something else
            used.remove(tile_num)
        # print(f"giving up on {tile_num}")
    # print(f"tried everything for {row} {col}")
    return None

filename, WIDTH, HEIGHT = ("input.txt", 12, 12)
# filename, WIDTH, HEIGHT = ("test.txt", 3, 3)
# filename, WIDTH, HEIGHT = ("test2.txt", 3, 2)

with open(filename) as f:
    tile_num = 0
    rows = []
    tiles = dict()

    for line in f:
        line = line.strip()
        if len(line) == 0:
            print(f"building tile {tile_num} from {len(rows)} rows")
            tiles[tile_num] = Tile(tile_num, rows)
            rows = []
            tile_num = 0
        elif line.startswith("Tile"):
            tile_num = int(line[5:-1])
        else:
            rows.append(line)

    if tile_num != 0 and len(rows) > 0:
        print(f"building tile {tile_num} from {len(rows)} rows")
        tiles[tile_num] = Tile(tile_num, rows)

print(len(tiles))

layout:typing.Sequence[typing.Sequence[typing.Optional[LayoutTile]]] = [[None for i in range(WIDTH)] for j in range(HEIGHT)]
used = set()
result = attempt_layout(layout, 0, 0, used)
if result:
    print("got result")
    print(layout[0][0].tile.tile_num * layout[0][-1].tile.tile_num * layout[-1][0].tile.tile_num * layout[-1][-1].tile.tile_num)
    for tile_row in layout:
        print("   ".join(f"{tile.tile.tile_num} {tile.orientation} {tile.rev}" for tile in tile_row))
else:
    print("failure")

# part 2

SEA_MONSTER_TEXT = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]
SEA_MONSTER_PIXELS = set((row, col) for row, line in enumerate(SEA_MONSTER_TEXT) for col, ch in enumerate(line) if ch == '#')
SEA_MONSTER_WIDTH = len(SEA_MONSTER_TEXT[0])
SEA_MONSTER_HEIGHT = len(SEA_MONSTER_TEXT)

final_image = set()
for row in range(HEIGHT):
    for col in range(WIDTH):
        for d_row in range(8):
            for d_col in range(8):
                if layout[row][col].pixel(d_row, d_col):
                    final_image.add((row * 8 + d_row, col * 8 + d_col))

assert len(final_image) == sum(1 for row in range(HEIGHT) for col in range(WIDTH) for d_row in range(1, 9) for d_col in range(1, 9) if layout[row][col].tile.pixels[d_row][d_col])

for row in range(HEIGHT * 8):
    for col in range(WIDTH * 8):
        if (row, col) in final_image:
            print('#', end='')
        else:
            print('.', end='')
        if col % 8 == 7: print(' ', end="")
    print()
    if row % 8 == 7: print()



def convert_to(row, col, orientation, rev, height, width):
    # rotate to the right orientation
    for i in range(orientation):
        row, col = width - 1 - col, row
        height, width = width, height
    # reverse if necessary
    if rev:
        col = width - 1 - col
    return row, col


def look_for(needle, needle_height, needle_width):
    found = []
    print(f"looking up to {HEIGHT * 8 - needle_height + 1}, {WIDTH * 8 - needle_width + 1}")
    for row in range(HEIGHT * 8 - needle_height + 1):
        for col in range(WIDTH * 8 - needle_width + 1):
            moved_needle = set((row + d_row, col + d_col) for (d_row, d_col) in needle)
            if moved_needle <= final_image:
                found.append((row, col))
    return found

monsters = dict()

for orientation, rev in ALL_ORIENTATIONS:
    # rotate the monster
    converted_monster = set(convert_to(row, col, orientation, rev, SEA_MONSTER_HEIGHT, SEA_MONSTER_WIDTH) for (row, col) in SEA_MONSTER_PIXELS)
    if orientation % 2:
        monster_height, monster_width = SEA_MONSTER_WIDTH, SEA_MONSTER_HEIGHT
    else:
        monster_height, monster_width = SEA_MONSTER_HEIGHT, SEA_MONSTER_WIDTH

    # look for sea monsters
    result = look_for(converted_monster, monster_height, monster_width)
    if result:
        print(f"{orientation} {rev} found {result}!")
        monster_pixels = set((row + d_row, col + d_col) for (row, col) in result for (d_row, d_col) in converted_monster)
        assert monster_pixels <= final_image
        monsters[orientation, rev] = monster_pixels
        for row in range(HEIGHT * 8):
            for col in range(WIDTH * 8):
                if (row, col) in monster_pixels:
                    print('O', end='')
                elif (row, col) in final_image:
                    print('#', end='')
                else:
                    print('.', end='')
            print()

        print(len(final_image - monster_pixels))

print({orientation: len(monsters[orientation]) for orientation in monsters})
