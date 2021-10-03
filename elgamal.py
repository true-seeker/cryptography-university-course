from Crypto.Util import number
from functools import wraps
from fast_power import fast_pow_module
from math import gcd as bltin_gcd


def coprime2(a, b):
    return bltin_gcd(a, b) == 1


def cache_gcd(f):
    cache = {}

    @wraps(f)
    def wrapped(a, b):
        key = (a, b)
        try:
            result = cache[key]
        except KeyError:
            result = cache[key] = f(a, b)
        return result

    return wrapped


@cache_gcd
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def prime_root(modulo):
    coprime_set = {num for num in range(1, modulo) if gcd(num, modulo) == 1}

    for g in range(1, modulo):
        if coprime_set == {pow(g, powers, modulo) for powers in range(1, modulo)}:
            return g


LENGTH = 18

M = 154654
print('M', M)
p = number.getPrime(LENGTH)
print('p', p)

g = prime_root(p)
print('g', g)

x = p + 1
while x >= p - 1:
    x = number.getPrime(LENGTH)
print('x', x)

y = fast_pow_module(g, x, p)
print('y', y)

k = -1
for i in range(p - 1):
    if coprime2(i, p - 1):
        k = i
print('k', k)
a = fast_pow_module(g, k, p)
b = fast_pow_module(y, k, p) * M % p

print('a,b', a, b)

M_decrypted = fast_pow_module(b * (a ** (p - 1 - x)), 1, p)

print('M_decrypted', M_decrypted)
