from math import sqrt


class SPoint:
    def __init__(self, y, a, r):
        self.a = a
        self.y = y
        self.r = r

        self.value = self.y * pow(self.a, self.r) % n
        self.key = r

    def __str__(self):
        return str(self.value)


class TPoint:
    def __init__(self, a, t, s):
        self.t = t
        self.a = a
        self.s = s

        self.value = pow(self.a, self.t * self.s) % n
        self.key = t * s

    def __str__(self):
        return str(self.value)


def find_in_list(ls, value):
    for i in ls:
        if i.value == value.value:
            return i, value

    return (None, None)


if __name__ == '__main__':
    n = 181
    # n = 19
    y = 62
    # y = 6
    a = 2
    S = []
    T = []

    s = round(sqrt(n))
    for r in range(0, s):
        S.append(SPoint(y, a, r))

    S = sorted(S, key=lambda x: x.value)

    for t in range(1, s + 1):
        T.append(TPoint(a, t, s))

    T = sorted(T, key=lambda x: x.value)

    for i in S:
        print(i, end=" ")
    print()
    for i in T:
        print(i, end=" ")
    print()

    tp = None
    sp = None
    for i in S:
        tp, sp = find_in_list(T, i)
        if tp is not None and sp is not None:
            break
    if tp is not None and sp is not None:
        x = tp.s * tp.t - sp.r
    print(f'x = {x}')
    print(f'log = {pow(a, x) % n}')
