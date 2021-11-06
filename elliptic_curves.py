import random


class EllipticCurve:
    def __init__(self, name, p, a, b, g, n, h):
        self.n = n
        self.h = h
        self.g = g
        self.b = b
        self.a = a
        self.p = p
        self.name = name

        print(name)


class Point:
    def __init__(self, x, y):
        self.y = y
        self.x = x

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False


curve = EllipticCurve(
    name='secp256k1',
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    a=0,
    b=7,
    g=Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
            0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    h=1)


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


def is_on_curve(point: Point):
    """Проверка принадлежности точки кривой"""
    if point is None:
        return True
    x, y = point.x, point.y

    return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0


def point_neg(point: Point):
    """Нахождение обратной точки"""
    assert is_on_curve(point)

    if point is None:
        return None

    x, y = point.x, point.y
    result = Point(x, -y % curve.p)

    assert is_on_curve(result)

    return result


def point_add(point1: Point, point2: Point):
    """Сложение двух точек"""
    assert is_on_curve(point1)
    assert is_on_curve(point2)

    if point1 is None:
        return point2
    if point2 is None:
        return point1

    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y

    if x1 == x2 and y1 != y2:
        return None

    if x1 == x2:
        m = (3 * x1 * x1 + curve.a) * modinv(2 * y1, curve.p)
    else:
        m = (y1 - y2) * modinv(x1 - x2, curve.p)

    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = Point(x3 % curve.p, -y3 % curve.p)

    assert is_on_curve(result)

    return result


def scalar_mult(k, point: Point):
    """Умножение k на точку"""
    assert is_on_curve(point)

    if k % curve.n == 0 or point is None:
        return None

    if k < 0:
        return scalar_mult(-k, point_neg(point))

    result = None
    addend = point

    while k:
        if k & 1:
            result = point_add(result, addend)

        addend = point_add(addend, addend)

        k >>= 1

    assert is_on_curve(result)

    return result


def make_keypair():
    private_key = random.randrange(1, curve.n)
    public_key = scalar_mult(private_key, curve.g)

    return private_key, public_key


alice_private_key, alice_public_key = make_keypair()
print(f"Закрытый ключ А: {hex(alice_private_key)}")
print(f"Открытый ключ А: ({hex(alice_public_key.x)}, {hex(alice_public_key.y)})\n")

bob_private_key, bob_public_key = make_keypair()
print(f"Закрытый ключ B: {hex(bob_private_key)}")
print(f"Открытый ключ B: ({hex(bob_public_key.x)}, {hex(bob_public_key.y)})\n")

s1 = scalar_mult(alice_private_key, bob_public_key)
s2 = scalar_mult(bob_private_key, alice_public_key)
assert s1 == s2
print(f'Вычисленный секрет от А и от Б: ({hex(s1.x)}, {hex(s1.y)})')
