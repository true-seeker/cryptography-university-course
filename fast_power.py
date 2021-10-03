def fast_pow_module(number: int, power: int, module: int):
    """Быстрое возведение в степень по модулю"""
    if power == 0:
        return 1

    z = fast_pow_module(number, power // 2, module)

    if power % 2 == 0:
        return z * z % module
    else:
        return number * z * z % module


if __name__ == '__main__':
    print(fast_pow_module(45634, 12336345634563, 15643545))
