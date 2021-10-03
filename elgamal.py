from Crypto.Util import number
from functools import wraps
from fast_power import fast_pow_module
from math import gcd as bltin_gcd
from hashlib import blake2b, blake2s, md5


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


def egcd(a: int, b: int):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    if a == 0:
        return (b, 0, 1)
    else:
        b_div_a, b_mod_a = divmod(b, a)
        g, x, y = egcd(b_mod_a, a)
        return (g, y - b_div_a * x, x)


def modinv(a: int, b: int) -> int:
    """return x such that (x * a) % b == 1"""
    g, x, _ = egcd(a, b)
    if g != 1:
        raise Exception('gcd(a, b) != 1')
    return x % b


def my_hash(message, max_value):
    hs = 0
    for i in str(message):
        hs += ord(i)
    while hs > max_value:
        hs = hs // 10
    return hs


LENGTH = 3

M = 'hfgdhdfghgfd'
p = number.getPrime(LENGTH * 4)
# p = 23
print('p', p)

m = my_hash(M, p - 1)
# m = 3
print('m', m)

k = -1
for i in range(3, p - 1):
    if coprime2(i, p - 1):
        k = i
        break
# k = 5
print('k', k)

x = p + 1
while x >= p - 1:
    x = number.getPrime(LENGTH)
# x = 7
print('x', x)

g = prime_root(p)
# g = 5
print('g', g)

y = fast_pow_module(g, x, p)
print('y', y)

r = fast_pow_module(g, k, p)
print('r', r)

k_minus_one = modinv(k, p - 1)
print('k_minus_one', k_minus_one)

s = ((m - x * r) * modinv(k, p - 1)) % (p - 1)
print('s', s)

print('podpis', M, r, s)

# ПРОВЕРКА
m = my_hash(M, p - 1)

print('0<r<p', 0 < r < p, )
print('0<s<p-1', 0 < s < p - 1)

print(fast_pow_module(y, r, p), fast_pow_module(r, s, p), (fast_pow_module(y, r, p) * fast_pow_module(r, s, p)) % p,
      fast_pow_module(g, m, p))
print((fast_pow_module(y, r, p) * fast_pow_module(r, s, p)) % p == fast_pow_module(g, m, p))
