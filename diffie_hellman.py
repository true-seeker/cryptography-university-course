from Crypto.Util import number
import random


def fast_pow_module(number: int, power: int, module: int):
    """Быстрое возведение в степень по модулю"""
    print(number, power, module)
    if power == 0:
        print('return 1 ')
        return 1

    z = fast_pow_module(number, power // 2, module)
    print(z)
    if power % 2 == 0:
        print(f'z * z % module {z * z % module}')
        return z * z % module
    else:
        print(f'number * z * z % module {number * z * z % module}')
        return number * z * z % module


print(fast_pow_module(2, 81, 100))
quit()
# g = random.randint(0, 2 ** 640)
# p = random.randint(0, 2 ** 640)

g = 1651333955009990372564182191498
p = 1928487810503845005694008034959
# g = 16513339
# p = 1928487


# a = number.getPrime(128)
# b = number.getPrime(128)
a = 228611989037558337665163358863720004159
# b = 2286
A = fast_pow_module(g, a, p)
# B = fast_pow_module(g, b, p)
# A = 1925269841609140841322999042114
B = 1140840186873478426066873723605

# A = 1968794657

B_1 = fast_pow_module(B, a, p)
# A_1 = fast_pow_module(A, b, p)

print('g', g)
print('p', p)
print('a', a)
# print('b', b)
print('A', A)
print('B', B)

print('B_1', B_1)
# print('A_1', A_1)

# print(B_1 == A_1)
