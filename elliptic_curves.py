import random


class Point:
    def __init__(self, x, y):
        self.y = y
        self.x = x

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def scalar_mult(self, k):
        res = self
        for i in range(k - 1):
            res += self
        return res

    def is_on_curve(self):
        global curve
        if self.x == 0 and self.y == 0:
            return True
        """Проверка принадлежности точки кривой"""
        x, y = self.x, self.y
        return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0

    def __add__(self, other):
        """Сложение двух точек"""
        if self.x == 0 and self.y == 0:
            return other
        if other.x == 0 and other.y == 0:
            return self

        x1, y1 = self.x, self.y
        x2, y2 = other.x, other.y

        if x1 == x2 and y1 == y2:
            l = (3 * x1 * x1 + curve.a) * modinv(2 * y1, curve.p)
        else:
            l = pow(y2 - y1, 1, curve.p) * modinv(x2 - x1, curve.p)
        x3 = pow(l * l - x1 - x2, 1, curve.p)
        y3 = pow(l * (x1 - x3) - y1, 1, curve.p)

        try:
            assert Point(x3, y3).is_on_curve()
        except AssertionError:
            return Point(0, 0)
        return Point(x3, y3)

    def __sub__(self, other):
        if self == Point(0, 0):
            k = 13
        else:
            k = curve.R.index(self) + 1
        if other == Point(0, 0):
            k1 = 13
        else:
            k1 = curve.R.index(other) + 1
        ind = k - k1 - 1
        if ind < 0:
            ind = ORDER + ind
        return curve.R[ind]

    def point_neg(self):
        """Нахождение обратной точки"""
        assert self.is_on_curve()

        if self is None:
            return None

        x, y = self.x, self.y
        result = Point(x, -y % curve.p)

        assert result.is_on_curve()

        return result

    def __str__(self):
        return f'({self.x};{self.y})'


class EllipticCurve:
    def __init__(self, a, b, g, p, n):
        self.p = p
        self.g = g
        self.b = b
        self.a = a
        self.n = n

    def make_ring(self):
        t = self.g
        self.R = [t, ]
        # print(t, end=" ")
        for i in range(self.n - 2):
            # for i in range(50):
            t += self.g
            # print(t, end=" ")
            self.R.append(t)
        self.R.append(Point(0, 0))


def egcd(a: int, b: int):
    """Расширенный алгоритм Евклида"""
    if a == 0:
        return b, 0, 1
    else:
        b_div_a, b_mod_a = divmod(b, a)
        g, x, y = egcd(b_mod_a, a)
        return g, y - b_div_a * x, x


def modinv(a: int, b: int) -> int:
    """Обратное по модулю"""
    g, x, y = egcd(a, b)
    if g == -1:
        x *= -1
        g *= -1

    return x % b


ORDER = 13


def make_keypair():
    private_key = random.randrange(1, ORDER - 1)
    public_key = curve.g.scalar_mult(private_key)

    return private_key, public_key


if __name__ == '__main__':

    curve = EllipticCurve(
        a=1,
        b=3,
        g=Point(1, ORDER),
        p=41,
        n=ORDER)
    curve.make_ring()

    letter = 'a'
    t = curve.g
    points_dict = {letter: t}
    letters_dict = {(t.x, t.y): letter}
    for i in range(ORDER - 2):
        t += curve.g
        letter = chr(ord(letter) + 1)
        points_dict[letter] = t
        letters_dict[(t.x, t.y)] = letter
    print('\nАлфавит', letters_dict)

    message = 'efabjkl'
    decrypted_message = ''
    count = 0
    for j in range(1):
        bob_private_key, bob_public_key = make_keypair()
        print(f"Закрытый ключ B: {bob_private_key}")
        print(f"Открытый ключ B: ({bob_public_key.x}, {bob_public_key.y})\n")
        for i in message:
            Pm = points_dict[i]

            k = random.randint(1, ORDER)
            # шифрование
            Cm = Point(curve.g.scalar_mult(k), Pm + (bob_public_key.scalar_mult(k)))
            # расшифрование

            a = Cm.y - Cm.x.scalar_mult(bob_private_key)

            decrypted_message += letters_dict[(a.x, a.y)]

    print(f'Расшифрованное сообщение: {decrypted_message}')
    assert message == decrypted_message
