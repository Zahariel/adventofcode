from parsy import seq, string

from parsing import number, split_on_blank
from utils import Coord2D, solve_diophantine

machines = []

with open("input.txt") as f:
    for a, b, p in split_on_blank(f):
        button_a = seq(string("Button A: X+") >> number << string(", Y+"), number).parse(a)
        button_b = seq(string("Button B: X+") >> number << string(", Y+"), number).parse(b)
        prize = seq(string("Prize: X=") >> number << string(", Y="), number).parse(p)
        machines.append((Coord2D(*button_a), Coord2D(*button_b), Coord2D(*prize)))


def win(machine, adjustment):
    a, b, prize = machine
    prize += Coord2D(adjustment, adjustment)
    # first solve x
    a_presses, b_presses, gcd = solve_diophantine(a.x, b.x)
    if prize.x % gcd != 0: return 0
    a_presses *= prize.x // gcd
    b_presses *= prize.x // gcd
    # now a_presses and b_presses gets us to the right x coordinate
    current_y = a.y * a_presses + b.y * b_presses
    up_action_a, up_action_b = -b.x // gcd, a.x // gcd
    up_motion = a.y * up_action_a + b.y * up_action_b
    # up_action presses moves the claw directly upward up_motion units; note that up_action_a is always negative
    if (prize.y - current_y) % up_motion != 0: return 0
    actions_needed = (prize.y - current_y) // up_motion
    return 3 * (a_presses + actions_needed * up_action_a) + (b_presses + actions_needed * up_action_b)


print(sum(win(machine, 0) for machine in machines))

ADJUSTMENT = 10000000000000

print(sum(win(machine, ADJUSTMENT) for machine in machines))
