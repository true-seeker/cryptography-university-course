from itertools import combinations
from math import sqrt, floor, exp, log, prod


def fast_pow_module(number: int, power: int, module: int) -> int:
    """Быстрое возведение в степень по модулю"""
    if power == 0:
        return 1

    z = fast_pow_module(number, power // 2, module)

    if power % 2 == 0:
        return z * z % module
    else:
        return number * z * z % module


def eratosthenes(n: int) -> list:
    """Решето Эратосфена"""
    sieve = list(range(n + 1))
    sieve[1] = 0
    for i in sieve:
        if i > 1:
            for j in range(i + i, len(sieve), i):
                sieve[j] = 0
    sieve1 = [x for x in sieve if x != 0]
    return sieve1


def gcd(a: int, b: int) -> int:
    """Алгоритм Евклида для НОД"""
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a


def factor(n) -> list:
    """Факторизация"""
    i = 2
    primfac = []
    if n < 0:
        primfac.append(-1)
        n = -n

    while i * i <= n:
        while n % i == 0:
            primfac.append(i)
            n = n // i
        i = i + 1
    if n > 1:
        primfac.append(n)
    return primfac


class QuadraticSieve:
    def __init__(self, n):
        self.n = n
        self.small_n = floor(sqrt(self.n))

    def find_factor_base(self, k) -> list:
        """Поиск факторной базы"""
        primes_list = eratosthenes(k)
        baza = {-1, }
        baza_P = exp(sqrt(log(k) * log(log(k))))

        for prime in primes_list:
            if prime > baza_P:
                break
            m = k % prime
            for i in range(prime):
                fpw = fast_pow_module(i, 2, prime)
                if fpw == m:
                    baza.add(prime)

        baza = sorted(baza)
        print('baza:', baza)
        return baza

    def perform(self):
        print('Поиск факторной базы')
        answer = set()
        factor_base = self.find_factor_base(self.n)

        # xor вектор
        xor_vector = {}
        # словарь с числами и степенями в разложении
        smooth_q = {}

        # расширяем диапазон до +- small_n/5 и пытаемся составить xor вектор
        for i in range(self.small_n // 5, self.small_n * 5):
            f = factor(i ** 2 - self.n)
            # проверка являются ли все числа в разложении гладким
            for j in f:
                if j > 20:
                    break
            else:
                powers = {}
                for j in f:
                    if powers.get(j) is not None:
                        powers[j] += 1
                    else:
                        powers[j] = 1

                vector = []
                # составление xor вектора
                for j in factor_base:
                    if powers.get(j) is None:
                        vector.append(0)
                    else:
                        if powers[j] % 2 == 0:
                            vector.append(0)
                        else:
                            vector.append(1)

                smooth_q[i] = powers
                xor_vector[i] = vector

        # выполнение xor над векторами
        for i in range(1, len(xor_vector)):
            for combination in set(combinations(xor_vector, i)):
                xor = [0 for _ in range(len(factor_base))]
                for key in combination:
                    for index, item in enumerate(xor_vector[key]):
                        xor[index] += item

                # если в xor есть хотя бы одно нечетное, то пропускаем
                for j in xor:
                    if j % 2 == 1:
                        break
                else:
                    x = prod(combination)
                    y = 1
                    # перемножаем степени для y
                    for j in combination:
                        for index, item in enumerate(xor_vector[j]):
                            if smooth_q[j].get(factor_base[index]) is not None:
                                y *= factor_base[index] ** smooth_q[j][factor_base[index]]
                    y = int(sqrt(y))

                    a = gcd(x + y, self.n)
                    b = gcd(x - y, self.n)
                    if a * b == self.n and a != self.n and b != self.n:
                        answer.add((a, b))
        return answer


if __name__ == '__main__':
    n = 465485
    q = QuadraticSieve(n)

    answer = q.perform()
    print(answer)
