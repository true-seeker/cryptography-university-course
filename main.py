def fast_pow_module(number: int, power: int, module: int) -> int:
    """Быстрое возведение в степень по модулю"""
    if power == 0:
        return 1

    z = fast_pow_module(number, power // 2, module)

    if power % 2 == 0:
        return z * z % module
    else:
        return number * z * z % module


if __name__ == '__main__':
    p = 149
    q = 211
    n = p * q
    e = 431
    phi = (p - 1) * (q - 1)
    t = 123
    c = pow(t, e, n)

    ci = pow(c, e, n)
    cim1 = c
    i = 0
    while ci != c:
        i += 1
        cim1 = ci
        ci = pow(cim1, e, n)

    print(f'Ans: {cim1}')
    print(i)
