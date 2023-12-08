import math

def manhattan(coords1, coords2):
    return sum(abs(x - y) for (x, y) in zip(coords1, coords2))


def chinese_remainder(equations):
    lcm = math.lcm(*(modulus for _, modulus in equations))


    inverses = [pow(modulus, -1, lcm//modulus) for _, modulus in equations]

    return sum(residue * inv * (lcm // modulus) for (residue, modulus), inv in zip(equations, inverses)) % lcm, lcm

