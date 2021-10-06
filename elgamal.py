from functools import wraps
from math import gcd as bltin_gcd

from Crypto.Util import number

from fast_power import fast_pow_module

LENGTH = 3


def coprime2(a, b):
    """Проверка """
    return bltin_gcd(a, b) == 1


def cache_gcd(f):
    """Декоратор для кэширования НОД"""
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
    """НОД"""
    while b != 0:
        a, b = b, a % b
    return a


def prime_root(modulo):
    """Первообразный корень"""
    coprime_set = {num for num in range(1, modulo) if gcd(num, modulo) == 1}

    for g in range(1, modulo):
        if coprime_set == {pow(g, powers, modulo) for powers in range(1, modulo)}:
            return g


def egcd(a: int, b: int):
    """Расширенный алгоритм Евклида"""
    if a == 0:
        return (b, 0, 1)
    else:
        b_div_a, b_mod_a = divmod(b, a)
        g, x, y = egcd(b_mod_a, a)
        return (g, y - b_div_a * x, x)


def modinv(a: int, b: int) -> int:
    """Обратное по модулю"""
    g, x, _ = egcd(a, b)
    if g != 1:
        raise Exception('gcd(a, b) != 1')
    return x % b


def my_hash(message, max_value):
    """Хэширование"""
    hs = 0
    for i in str(message):
        hs += ord(i)
    while hs > max_value:
        hs = hs // 10
    return hs


def sign(message):
    p = number.getPrime(LENGTH * 4)

    m = my_hash(message, p - 1)

    k = -1
    for i in range(3, p - 1):
        if coprime2(i, p - 1):
            k = i
            break

    x = p + 1
    while x >= p - 1:
        x = number.getPrime(LENGTH)

    g = prime_root(p)

    y = fast_pow_module(g, x, p)

    r = fast_pow_module(g, k, p)

    k_minus_one = modinv(k, p - 1)

    s = ((m - x * r) * modinv(k, p - 1)) % (p - 1)

    m = my_hash(message, p - 1)
    print('p', p)
    print('m', m)
    print('k', k)
    print('x', x)
    print('g', g)
    print('y', y)
    print('r', r)
    print('k^-1', k_minus_one)
    print('s', s)
    return p, g, y, r, s, m


def check_sign(p, g, y, r, s, m):
    # ПРОВЕРКА
    if 0 < r < p and \
            0 < s < p - 1 and \
            (fast_pow_module(y, r, p) * fast_pow_module(r, s, p)) % p == fast_pow_module(g, m, p):
        return True
    else:
        print('0<r<p', 0 < r < p, )
        print('0<s<p-1', 0 < s < p - 1)
        print((fast_pow_module(y, r, p) * fast_pow_module(r, s, p)) % p == fast_pow_module(g, m, p))
        return False


def encrypt(message):
    encrypted = ''
    p = number.getPrime(LENGTH * 4)
    g = prime_root(p)
    x = p + 1
    while x >= p - 1:
        x = number.getPrime(LENGTH)
    y = fast_pow_module(g, x, p)

    for i in message:
        k = -1
        for j in range(3, p - 1):
            if coprime2(j, p - 1):
                k = j
                break

        a = fast_pow_module(g, k, p)

        b = (fast_pow_module(y, k, p) * ord(i)) % p
        encrypted += chr(a) + chr(b)
    return encrypted, x, p


def decrypt(encrypted, x, p):
    message = ''
    while len(encrypted) > 0:
        a = encrypted[0]
        b = encrypted[1]
        encrypted = encrypted[2:]

        m = (ord(b) * fast_pow_module(ord(a), p - 1 - x, p)) % p

        message += chr(m)

    return message


if __name__ == '__main__':
    message_to_sign = 'Hello'

    encrypted_message, _x, _p = encrypt(message_to_sign)
    print('encrypted_message: ', encrypted_message)

    decrypted_message = decrypt(encrypted_message, _x, _p)
    print('decrypted_message', decrypted_message)

    p, g, y, r, s, m = sign(message_to_sign)

    if check_sign(p, g, y, r, s, m):
        print('Подпись успешно проверена')
    else:
        raise Exception('Проверка не пройдена')
