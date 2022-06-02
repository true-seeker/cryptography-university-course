import random
from Crypto.Util import number


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x};{self.y})'


class Polynom:
    def __init__(self, n, p):
        self.n = n
        self.p = p
        self.a = []
        self.points = []

    def generate_a(self):
        for _ in range(self.n + 1):
            self.a.append(random.randint(1, self.p - 1))
        # print(self.a)

    def calculate_points(self):
        for x in range(self.p):
            y = 0
            for j in range(self.n + 1):
                y += self.a[j] * pow(x, j)
            y %= self.p
            self.points.append(Point(x, y))

    def build_secret(self, points, a_index):
        sct = 0
        for xi in points:
            mult = xi.y
            for j in points:
                if xi == j:
                    continue
                mult *= (a_index - j.x) * pow((xi.x - j.x), -1, self.p)
            mult %= self.p
            # print(mult)
            sct += mult
        sct %= self.p

        return sct

    def __str__(self):
        t = ''
        for i in self.points:
            t += f'{i} '
        return t


if __name__ == '__main__':
    for _ in range(10):
        n = random.randint(3, 100)
        p = number.getPrime(10)
        # n = 3
        # p = 13
        pol = Polynom(n, p)
        pol.generate_a()
        secret_index = random.choice(range(len(pol.a)))
        secret_index = 0
        # pol.a = [4, 9, 4, 1]
        pol.calculate_points()
        m = n + 1
        random_points = random.sample(pol.points, m)
        # random_points = [Point(3, 3), Point(8, 12), Point(9, 7), Point(6, 2)]
        secret = pol.build_secret(random_points, secret_index)

        if pol.a[secret_index] != secret:
            print(n, p, [str(i) for i in random_points], pol.a, secret)
        else:
            print(n, p, pol.a[secret_index] == secret)
