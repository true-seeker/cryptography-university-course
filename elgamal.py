from functools import wraps
from math import gcd as bltin_gcd

from Crypto.Util import number

import base64

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

    y = pow(g, x, p)

    r = pow(g, k, p)

    k_minus_one = modinv(k, p - 1)

    s = ((m - x * r) * modinv(k, p - 1)) % (p - 1)

    m = my_hash(message, p - 1)
    # print('p', p)
    # print('m', m)
    # print('k', k)
    # print('x', x)
    # print('g', g)
    # print('y', y)
    # print('r', r)
    # print('k^-1', k_minus_one)
    # print('s', s)
    return p, g, y, r, s, m


def check_sign(p, g, y, r, s, m):
    # ПРОВЕРКА
    if 0 < r < p and \
            0 < s < p - 1 and \
            (pow(y, r, p) * pow(r, s, p)) % p == pow(g, m, p):
        return True
    else:
        # print('0<r<p', 0 < r < p, )
        # print('0<s<p-1', 0 < s < p - 1)
        print((pow(y, r, p) * pow(r, s, p)) % p == pow(g, m, p))
        return False


def encrypt(message, key, x):
    encrypted = []
    y, g, p = key
    # p = number.getPrime(7)
    # g = prime_root(p)
    # x = p + 1
    # while x >= p - 1:
    #     x = number.getPrime(LENGTH)
    # y = pow(g, x, p)
    # k = -1
    print(y, g, p, x, sep=', ')
    for j in range(3, p - 1):
        if coprime2(j, p - 1):
            k = j
            break

    for i in message:
        a = pow(g, k, p)
        # b = (pow(y, k, p) * ord(i)) % p
        b = (pow(y, k, p) * i) % p
        encrypted.append(a)
        encrypted.append(b)
    return encrypted, x, p


def decrypt(encrypted, x, p):
    message = []
    while len(encrypted) > 0:
        a = encrypted[0]
        b = encrypted[1]
        encrypted = encrypted[2:]

        m = (b * pow(a, p - 1 - x, p)) % p

        message.append(m)

    return message


if __name__ == '__main__':
    a = 10
    b = 20
    tt = 100
    l = 75
    k = (21, 5, 97)  # 5
    ka = (116, 3, 127)  # 5
    kb = (51, 5, 103)  # 7
    s1 = f'{tt}_{l}_{k}_{b}'.encode()
    # for i in s1:
    #     print(i, end=' ')
    # print()
    s2 = f'{tt}_{l}_{k}_{a}'.encode()
    d1, _x1, _p1 = encrypt(s1, ka, 5)
    d2, _x2, _p2 = encrypt(s2, kb, 7)
    d1_decrypted = decrypt(d1, _x1, _p1)
    d2_decrypted = decrypt(d2, _x2, _p2)

    print('s1:', s1)
    print('s1: ', [i for i in s1])
    print('d1: ', d1)
    print('d1_decrypted:', d1_decrypted)
    print('d1: ', end='')
    d1_t = ''
    for i in d1:
        print(chr(i), end='')
        d1_t += chr(i)

    print('\n')
    print('s2:', s2)
    print('s2: ', [i for i in s2])
    print('d2: ', d2)
    print('d2_decrypted:', d2_decrypted)
    print('d2: ', end='')
    d2_t = ''
    for i in d2:
        d2_t += chr(i)
        print(chr(i), end='')
    print()
    sss = base64.b64encode(d1_t.encode())
    print(base64.b64decode(sss).decode('utf-8'))
    print(base64.b64encode(d1_t.encode()).decode(), base64.b64encode(d2_t.encode()).decode('utf-8'), sep='|')
    # p, g, y, r, s, m = sign(message_to_sign)
    #
    # if check_sign(p, g, y, r, s, m):
    #     print('Подпись успешно проверена')
    # else:
    #     raise Exception('Проверка не пройдена')

'G+C7jRvHqRvHqRvavxvgtJAbzJkb2r8b4KaAG+CvoBvgu40b4KijG+C0kBvgtp0bxYYb4KOzG+C2nRvFhhvgr6Ab3LYbLBvcthvakxvavxvgr6Abx6k='
'G8u7G8KpG8KpG+C7kRvElhvgsYMb4LuRG+C2uxvVjRvLuxvNqBvElhvcshvgq7wb3p8b3LIb4Ku8G9WNG9a6G+C6lRvWuhs8G+C7kRvVjRvCqQ=='
'G8u7G8KpG8KpG+C7kRvElhvgsYMb4LuRG+C2uxvVjRvLuxvNqBvElhvcshvgq7wb3p8b3LIb4Ku8G9WNG9a6G+C6lRvWuhs8G+C7kRvVjRvCqQ==|xZfKr8WXwpzFl8KcxZfdpMWX26LFl8q8xZfdpMWXwoLFl9OCxZfKr8WXwrbFl9uixZfCj8WXaMWX25XFl8KPxZdoxZfTgsWXy4nFl9OPxZfLicWXypXFl92kxZfKr8WXwpw='
