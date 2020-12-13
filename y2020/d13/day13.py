import functools
import operator

with open("input.txt") as f:
    now = int(f.readline().strip())
    buses = [(int(bus), idx) for idx, bus in enumerate(f.readline().strip().split(",")) if bus != "x"]

wait, bus = min((-now % bus, bus) for bus, idx in buses)

print(bus, wait, bus * wait)

print(buses)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def CRT(eqns):
    M = functools.reduce(operator.mul, (m for m, a in eqns))
    return sum(-a * (M//m) * modinv(M//m, m) for m, a in eqns) % M

crt = CRT(buses)
print(crt)

