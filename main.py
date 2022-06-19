import re
from functools import reduce
from math import gcd
from random import randrange


# from Crypto.Util import number


def isprime(n):
    return re.compile(r'^1?$|^(11+)\1+$').match('1' * n) is None


def gen_prime(start, end):
    return (x for x in range(start, end) if isprime(x))


def rand_prime(start, end):
    while True:
        p = randrange(start, end, 2)
        if all(p % i != 0 for i in range(3, int((p ** 0.5) + 1), 2)):
            return p


def fi(n):
    f = n
    if n % 2 == 0:
        while n % 2 == 0:
            n = n // 2
        f = f // 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n = n // i
            f = f // i
            f = f * (i - 1)
        i = i + 2
    if n > 1:
        f = f // n
        f = f * (n - 1)
    return f


def coprime(a, b):
    return gcd(a, b) == 1


def calculate_h_list(val):
    h_list = []
    primes = gen_prime(3, val ** 2)
    for digit, prime in zip(bin(val)[2:][::-1], primes):
        if digit == '1':
            h_list.append(prime)
    return h_list


class Bill:
    def __init__(self, value):
        self.value = value
        self.h_list = []

        self.h_list = calculate_h_list(self.value)
        self.h = reduce(lambda a, b: a * b, self.h_list)
        print(f'Купюра {value}: h = {self.h_list} = {self.h}\n')

    def blind_sign(self, val):
        # oh = pow(self.h, -1, (p - 1) * (q - 1))
        #
        # print(pow(val, pow(self.h, -1, n), n))
        # return pow(val, pow(self.h, -1, (p - 1) * (q - 1)), (p - 1) * (q - 1))

        return pow(val, pow(self.h, -1, fn), fn)


if __name__ == '__main__':
    # p = rand_prime(10, 50)
    # q = rand_prime(10, 50)
    p = 47
    q = 17  # r1, r2 = 23
    # while not coprime(p, q):
    #     p = rand_prime(500, 5000)
    #     q = rand_prime(500, 5000)
    # p = 509
    # q = 827
    print(f'p: {p}')
    print(f'q: {q}')
    # n = (p - 1) * (q - 1)
    n = p * q
    fn = (p - 1) * (q - 1)
    print(f'n: {n}')
    # разряд числа
    value_digit = 4

    bill = Bill(15)

    number1 = 153

    blind_signed_number1 = bill.blind_sign(number1)
    print(f'Шаг 2:\nblind_signed_number1: {blind_signed_number1}\n')

    shag4_number1 = 402
    shag4_number2 = 722

    bill2 = Bill(5)

    # blind_signed_number_t = bill2.blind_sign(shag4_number2)
    blind_signed_number_t = pow(shag4_number2, pow(bill2.h, -1, fn), n)

    print(f'Шаг 5:\nblind_signed_number_t: {blind_signed_number_t}')
