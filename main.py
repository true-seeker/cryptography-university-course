import random
from math import gcd
from Crypto.Util import number


def coprime(a, b):
    return gcd(a, b) == 1


m = random.randint(2, 2 ** 16)
print(f'm: {m}')
while True:
    p = number.getPrime(20)
    ba = random.randint(2, p)
    while not coprime(ba, p):
        ba = random.randint(2, p)

    bb = random.randint(2, p)
    while not coprime(bb, p):
        bb = random.randint(2, p)

    try:
        aa = pow(ba, -1, p - 1)
    except ValueError:
        continue

    try:
        ab = pow(bb, -1, p - 1)
    except ValueError:
        continue
    else:
        break
print(f'p: {p}')
print(f'ba: {ba}')
print(f'bb: {bb}')
print(f'aa: {aa}')
print(f'aa: {ab}')

x1 = pow(m, aa, p)
print(f'x1: {x1}')
x2 = pow(x1, ab, p)
print(f'x2: {x2}')
x3 = pow(x2, ba, p)
print(f'x3: {x3}')
x4 = pow(x3, bb, p)
print(f'x4: {x4}')

print(x4 == m)
