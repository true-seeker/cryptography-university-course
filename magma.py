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


class CipherKey:
    def __init__(self, key: int):
        if key > 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff or key < 0x1000000000000000000000000000000000000000000000000000000000000000:
            raise ValueError("Число не 256 бит")

        self.key = key
        self.str_key = hex(key).replace('0x', '')
        self.count = 0
        self.term = 1

    def __call__(self, *args, **kwargs):
        self.term = args[0]
        if args[0] == -1:
            self.count = 31
        else:
            self.count = 0
        return self

    def __iter__(self):
        return self

    def __next__(self):
        if 0 <= self.count < 24:
            result = int(self.str_key[8 * (self.count % 8):8 * (self.count % 8 + 1)], 16)
            self.count += self.term
            return result
        elif 24 <= self.count < 32:
            result = int(self.str_key[8 * (8 - self.count % 8 - 1):8 * (8 - self.count % 8)], 16)
            self.count += self.term
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

    def get_as_int(self) -> int:
        """Преобразование в целое число"""
        return self.left_part * 0x10 ** 8 + self.right_part

    def magma_crypt(self, cipher_key: CipherKey, is_decrypt: bool):
        """
        Шифрование/дешифрование
        :param cipher_key: ключ
        :param is_decrypt: False, если зашифрование, True, если расшифрование
        :return: Number64
        """
        counter = 0
        iter_direction = -1 if is_decrypt else 1

        this_right = self.right_part
        this_left = self.left_part

        for round_key in cipher_key(iter_direction):
            # print(counter, hex(round_key), hex(self.left_part), hex(self.right_part))
            saved_left = this_left
            saved_right = this_right
            this_left = this_right

            this_right = modulo_addition(this_right, round_key, 2 ** 32)
            # print(hex(self.right_part))
            this_right = pi_transform(this_right)
            # print(hex(self.right_part))

            this_right = left_num_shift(this_right, 11)
            # print(hex(self.right_part))
            this_right = this_right ^ saved_left
            # print(hex(self.right_part))
            if counter == 31:
                this_left = this_right
                this_right = saved_right
            counter += 1

        return Number64(this_left * 0x10 ** 8 + this_right)


def pi_transform(number: int) -> int:
    """Преобразование пи"""
    str_num = hex(number).replace('0x', '')
    str_num = (8 - len(str_num)) * '0' + str_num

    result = ''
    for i in range(len(str_num)):
        result += hex(Pi[i][int(str_num[i], 16)]).replace('0x', '')
    return int(result, 16)


def left_num_shift(number: int, value: int) -> int:
    """Циклический сдвиг на value знаков влево"""
    str_num = bin(number).replace('0b', '')
    str_num = (32 - len(str_num)) * '0' + str_num
    for i in range(value):
        str_num = str_num[1:] + str_num[0]
    return int(str_num, 2)


def modulo_addition(a: int, b: int, m: int) -> int:
    """Сложение по модулю m"""
    return (a + b) % m


if __name__ == '__main__':
    num = Number64(0xfedcba9876543210)
    full_key = CipherKey(0xffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff)

    encrypted_number = num.magma_crypt(full_key, False)
    print(encrypted_number)

    decrypted_number = encrypted_number.magma_crypt(full_key, True)
    print(decrypted_number)
