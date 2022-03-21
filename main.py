class FEAL:
    BLOCK_LENGTH = 8

    def __init__(self, message: str, key: str):
        assert len(message) == self.BLOCK_LENGTH
        assert len(key) == self.BLOCK_LENGTH

        self.message = []
        for i in message:
            self.message.append(ord(i))

        self.key = []
        for i in key:
            self.key.append(ord(i))

    def xor(self, a: list, b: list):
        result = []
        for ai, bi in zip(a, b):
            result.append(ai ^ bi)
        return result

    def encrypt(self):
        left_part = self.message[:self.BLOCK_LENGTH // 2]
        right_part = self.message[self.BLOCK_LENGTH // 2:]
        left_part = self.xor(left_part,)
        print(left_part)
        print(right_part)


if __name__ == '__main__':
    m = 'alohntzp'
    key = '12345678'
    f = FEAL(m, key)

    f.encrypt()
