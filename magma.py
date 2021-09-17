class CipherKey:
    def __init__(self, key: int):
        if key > 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff or key < 0x1000000000000000000000000000000000000000000000000000000000000000:
            raise ValueError("Число не 256 бит")

        self.key = key
        self.str_key = hex(key).removeprefix('0x')
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < 24:
            result = int(self.str_key[8 * (self.count % 8):8 * (self.count % 8 + 1)], 16)
            self.count += 1
            return result
        elif 24 <= self.count < 32:
            result = int(self.str_key[8 * (8 - self.count % 8 - 1):8 * (8 - self.count % 8)], 16)
            self.count += 1
            return result
        else:
            raise StopIteration


class Number64:
    def __init__(self, number: int):
        if number > 0xffffffffffffffff or number < 0x1000000000000000:
            raise ValueError("Число не 64 бит")
        self.left_part = number // 0x10 ** 8
        self.right_part = number % 0x10 ** 8

    def __str__(self):
        return f'{hex(self.left_part)}|{hex(self.right_part)}'

    def encrypt(self, cipher_key: CipherKey) -> int:
        counter = 0
        for round_key in cipher_key:
            # print(counter, hex(round_key), hex(self.left_part), hex(self.right_part))
            saved_left = self.left_part
            saved_right = self.right_part
            self.left_part = self.right_part

            self.right_part = modulo_addition(self.right_part, round_key)
            # print(hex(self.right_part))
            self.right_part = pi_transform(self.right_part)  # 1108F15A
            # print(hex(self.right_part))

            self.right_part = num_shift(self.right_part, 11)  # 478ad088
            # print(hex(self.right_part))
            self.right_part = self.right_part ^ saved_left
            # print(hex(self.right_part))
            if counter == 31:
                self.left_part = self.right_part
                self.right_part = saved_right
            counter += 1

        return self.left_part * 0x10 ** 8 + self.right_part


Pi = [
    (1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2),
    (8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7),
    (5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0),
    (7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12),
    (12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11),
    (11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0),
    (6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15),
    (12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1)
]


def pi_transform(number: int) -> int:
    str_num = hex(number).removeprefix('0x')
    str_num = (8 - len(str_num)) * '0' + str_num

    result = ''
    for i in range(len(str_num)):
        result += hex(Pi[i][int(str_num[i], 16)]).removeprefix('0x')
    return int(result, 16)


def num_shift(number: int, value: int) -> int:
    str_num = bin(number).removeprefix('0b')
    str_num = (32 - len(str_num)) * '0' + str_num
    for i in range(value):
        str_num = str_num[1:] + str_num[0]
    return int(str_num, 2)


def modulo_addition(a: int, b: int) -> int:
    return (a + b) % (2 ** 32)


if __name__ == '__main__':
    a = Number64(0xfedcba9876543210)
    full_key = CipherKey(0xffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff)
    # print(hex(pi_transform(a.left_part)))
    # print(hex(modulo_addition(a.left_part,a.right_part)))
    # print(hex(num_shift(a.left_part, 11)))
    # print(hex(0x68695433 << 11))
    # quit()
    print(hex(a.encrypt(full_key)))
