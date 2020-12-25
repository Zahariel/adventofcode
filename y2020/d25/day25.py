
with open("input.txt") as f:
    card_key = int(f.readline().strip())
    door_key = int(f.readline().strip())

INITIAL_SUBJECT = 7
MODULUS = 20201227

# card_key = 7 ** card_loops
# door_key = 7 ** door_loops
# encryption = card_key ** door_loops = door_key ** card_loops = 7 ** (card_loops * door_loops)


def discrete_log(target, base, modulus):
    value = 1
    power = 0
    while value != target:
        value *= base
        value %= modulus
        power += 1
        if power >= modulus: return None
    return power

print(card_key, door_key)
card_loops = discrete_log(card_key, INITIAL_SUBJECT, MODULUS)
print(card_loops)
encryption_key = pow(door_key, card_loops, MODULUS)
print(encryption_key)


