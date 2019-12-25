from y2019.intcode import InteractiveAsciiComp
from itertools import combinations

with open("input.txt") as f:
    cells = [int(c) for c in f.readline().strip().split(",")]


ITEMS = [
    #"antenna",
    "asterisk",
    "astronaut ice cream",
    "dark matter",
    "fixed point",
    "hologram",
    "monolith",
    "ornament",
]

ITEM_COLLECTION = [
    "east",
    #"take antenna", # the antenna is too heavy by itself and is therefore useless
    "north",
    "west",
    "west",
    "take astronaut ice cream",
    "east",
    "south",
    "take hologram",
    "north",
    "east",
    "north",
    "take asterisk",
    "south",
    "south",
    "east",
    "take ornament",
    "north",
    "west",
    "take fixed point",
    "east",
    "south",
    "west",
    "west",
    "south",
    "south",
    "south",
    "take dark matter",
    "north",
    "west",
    "north",
    "take monolith",
    "north",
    "north",
    *("drop " + item for item in ITEMS)
]

def do_macro():
    yield from ITEM_COLLECTION

    for size in range(1, len(ITEMS)):
        for comb in combinations(ITEMS, size):
            yield from ["take " + item for item in comb]
            print("<<<trying", comb, ">>>")
            yield "east"
            # i don't know what happens when it succeeds, so i can just "enter" through until it does
            input()
            yield from ["drop " + item for item in comb]

    while True:
        yield input()

comp = InteractiveAsciiComp(cells, input_fn=do_macro().__next__)

comp.run()

# the answer ended up being asterisk, astronaut ice cream, fixed point, ornament
# also it turns out that the intcomp just exits when you pass the test
