def convert_python_bin(python_bin: str) -> str:
    return python_bin.replace('0b', (8 - (len(python_bin) - 2)) * '0')


def middle_string_swap(string_to_swap: str) -> str:
    middle_index = int(len(string_to_swap) / 2)
    first_half = string_to_swap[:middle_index]
    string_to_swap = string_to_swap[middle_index:] + first_half

    return string_to_swap


def xor(x: str, y: str) -> str:
    n = int(x, 2) ^ int(y, 2)
    n = convert_python_bin(bin(n))
    return n


if __name__ == '__main__':
    print(convert_python_bin('0b11'))
    print(middle_string_swap('00001111'))
    print(xor('10100101', '111111'))
