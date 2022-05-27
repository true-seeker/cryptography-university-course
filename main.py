import random
from math import gcd

from Crypto.Util import number


def coprime(a, b):
    return gcd(a, b) == 1


def hash(*args):
    result = 0
    for i in args:
        result ^= i
    return result


class Sign:
    def __init__(self, j, y, z):
        self.z = z
        self.y = y
        self.j = j

    def __str__(self):
        return f'z: {self.z}, y: {self.y}, j: {self.j}'


class SecretKey:
    def __init__(self, n, t, l):
        self.n = n
        self.t = t
        self.j = 0
        self.l = l
        self.lst = []

    def upd(self):
        if self.j == self.t + 1:
            return

        temp = [pow(i, 2, self.n) for i in self.lst[self.j]]
        self.lst.append(temp)
        self.j += 1

    def sign(self, message: int) -> Sign:
        generator = random.randint(2, self.n)
        while not coprime(self.n, generator):
            generator = random.randint(2, self.n)

        # print([pow(generator, i, self.n) for i in range(1, self.l + 1)])
        r = random.choice([pow(generator, i, self.n) for i in range(1, self.l + 1)])
        # print(r)
        y = pow(r, 2 * (self.t + 1 - self.j), self.n)
        c = []
        z = r % self.n
        for i in range(self.l):
            c.append(hash(i, y, message))
            z *= pow(self.lst[self.j][i], c[i], self.n)
        z = z % self.n

        return Sign(self.j, y, z)

    def __str__(self):
        return f'N: {self.n}, T: {self.t}, j: {self.j}, SKj: {self.lst}'


class PublicKey:
    def __init__(self, n, t, l):
        self.n = n
        self.t = t
        self.l = l
        self.lst = []

    def verify(self, message, sign: Sign):
        c = []
        temp = sign.y % self.n
        for i in range(self.l):
            c.append(hash(i, sign.y, message))
            temp *= pow(self.lst[i], c[i], self.n)
        temp = temp % self.n

        # print(pow(sign.z, 2 * (self.t + 1 - sign.j), self.n))
        # print(temp)
        return pow(sign.z, 2 * (self.t + 1 - sign.j), self.n) == temp

    def __str__(self):
        return f'N: {self.n}, T: {self.t}, PK: {self.lst}'


def kg(k, l, t):
    p = 0
    q = 0
    while p % 4 != 3:
        p = number.getPrime(k // 2)

    while q % 4 != 3:
        q = number.getPrime(k // 2)

    n = p * q
    sk = SecretKey(n, t, l)
    pk = PublicKey(n, t, l)

    generator = random.randint(2, n)
    while not coprime(n, generator):
        generator = random.randint(2, n)

    sk.lst.append([pow(generator, i, n) for i in range(1, l + 1)])

    pk.lst = ([pow(i, 2 * (t + 1), n) for i in sk.lst[0]])

    return sk, pk


if __name__ == '__main__':
    T = 7
    l = 10
    secret_key, public_key = kg(10, l, T)
    print(f'secret_key: {secret_key}')
    print(f'public_key: {public_key}')
    for i in range(T):
        message = random.randint(1, 2 ** 32)
        # print(f'message: {message}')

        sign = secret_key.sign(message)
        # print(f'sign: {sign}')
        print(public_key.verify(message, sign))
        secret_key.upd()
        # print(f'secret_key: {secret_key}')
