from Crypto.Util import number
from math import gcd as bltin_gcd
import random

import matplotlib.pyplot as plt


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


def coprime2(a, b):
    """Проверка """
    return bltin_gcd(a, b) == 1


def fast_pow_module(number: int, power: int, module: int):
    """Быстрое возведение в степень по модулю"""
    if power == 0:
        return 1

    z = fast_pow_module(number, power // 2, module)

    if power % 2 == 0:
        return z * z % module
    else:
        return number * z * z % module


def generate():
    p = 0
    q = 0
    x = 0

    while p % 4 != 3:
        p = number.getPrime(LENGTH)
    while q % 4 != 3:
        q = number.getPrime(LENGTH)
    # p = 7
    # q = 19
    n = p * q
    # print('p', p)
    # print('q', q)
    # print('n', n)

    j = random.randint(3, n - 1)
    while not coprime2(j, n - 1):
        j = random.randint(3, n - 1)

    x = j
    # x = 100
    # print('x', x)

    x0 = fast_pow_module(x, 2, n)
    # print('x0', x0)

    b_list = []
    for j in range(50):
        x_i = fast_pow_module(x0, 2, n)
        b_i = x_i % 2
        b_list.append(str(b_i))
        x0 = x_i

    num = int(''.join(b_list), 2)

    return num


LENGTH = 10
num_dict = {}
fig = plt.figure()

print('Генерирую')
for i in range(50000):
    generated_num = generate()
    if num_dict.get(generated_num) is None:
        num_dict[generated_num] = 1
    else:
        num_dict[generated_num] += 1

print('Строю')
plt.scatter(*zip(*num_dict.items()))

print(num_dict)
plt.grid(True)
plt.show()
