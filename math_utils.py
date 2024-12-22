import math


def chinese_remainder(equations):
    """Solves x = r1 (mod m1); x = r2 (mod m2); ... given (r1, m1), (r2, m2), ...
    Returns x, M = lcm(m1, m2, ...)"""
    lcm = math.lcm(*(modulus for _, modulus in equations))


    inverses = [pow(modulus, -1, lcm//modulus) for _, modulus in equations]

    return sum(residue * inv * (lcm // modulus) for (residue, modulus), inv in zip(equations, inverses)) % lcm, lcm


def solve_diophantine(a, b):
    """Solves a * s + b * t = gcd(a, b) = r"""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r > 0:
        q = old_r // r
        old_r, r = r, old_r % r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_s, old_t, old_r
