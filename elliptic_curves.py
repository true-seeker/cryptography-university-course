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
        """Умножение k на точку"""
        assert self.is_on_curve()

        if k % curve.n == 0 or self is None:
            return None

        if k < 0:
            return self.point_neg().scalar_mult(-k)

        addend = self
        result = addend

        while k:

            if k & 1:
                result = result + addend

            addend = addend + addend

            k >>= 1

        assert result.is_on_curve()

        return result

    def is_on_curve(self):
        global curve
        """Проверка принадлежности точки кривой"""
        if self is None:
            return True
        x, y = self.x, self.y
        return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0

    def __add__(self, other):
        """Сложение двух точек"""
        assert self.is_on_curve()
        assert other.is_on_curve()

        if self is None:
            return other
        if other is None:
            return self

        x1, y1 = self.x, self.y
        x2, y2 = other.x, other.y

        if x1 == x2 and y1 != y2:
            return None

        if x1 == x2:
            m = (3 * x1 * x1 + curve.a) * modinv(2 * y1, curve.p)
        else:
            m = (y1 - y2) * modinv(x1 - x2, curve.p)

        x3 = m * m - x1 - x2
        y3 = y1 + m * (x3 - x1)
        result = Point(x3 % curve.p, -y3 % curve.p)

        assert result.is_on_curve()

        return result

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
    def __init__(self, a, b, g, p):
        self.p = p
        self.g = g
        self.b = b
        self.a = a
        self.n = 4


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

    assert g == 1
    return x % b


def make_keypair():
    private_key = random.randrange(1, curve.n)
    public_key = curve.g.scalar_mult(private_key)

    return private_key, public_key


curve = EllipticCurve(
    a=1,
    b=3,
    g=Point(1, 13),
    p=41)

alice_private_key, alice_public_key = make_keypair()

alice_private_key = 1
alice_public_key = Point(7, 5)
print(f"Закрытый ключ А: {alice_private_key}")
print(f"Открытый ключ А: ({alice_public_key.x}, {alice_public_key.y})\n")

# bob_private_key, bob_public_key = make_keypair()
# print(f"Закрытый ключ B: {bob_private_key}")
# print(f"Открытый ключ B: ({bob_public_key.x}, {bob_public_key.y})\n")

bob_public_key = Point(27, 19)

s1 = bob_public_key.scalar_mult(alice_private_key)
# s2 = alice_public_key.scalar_mult(bob_private_key)
print(f'Вычисленный секрет от А и от Б: ({s1})')
