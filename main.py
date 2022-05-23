import json
import time

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import random
import rsa

HASHING_ALGORYTHM = 'SHA-1'


class Pretender:
    def __init__(self, ident, private_key):
        self.private_key = private_key
        self.ident = ident


class Verifier:
    def __init__(self, ident, public_key):
        self.public_key = public_key
        self.ident = ident


if __name__ == '__main__':

    # P и V обмениваются ключами
    print('P и V обмениваются ключами\n')
    public_rsa_key, private_rsa_key = rsa.newkeys(512)
    p = Pretender(random.randint(1, 2 ** 16), private_rsa_key)
    v = Verifier(random.randint(1, 2 ** 16), public_rsa_key)

    # V генерирует случайное число
    print('V генерирует случайное число')
    rv = random.randint(2 ** 32, 2 ** 48)
    print(f'rv: {rv}\n')

    # V (Rv)-> P

    # P генерирует случайное число
    print('P генерирует случайное число')
    rp = random.randint(2 ** 32, 2 ** 48)
    print(f'rp: {rp}\n')

    # P составляет сообщение
    print('P составляет сообщение')
    message = json.dumps({"rv": rv,
                          "rp": rp,
                          'Vid': v.ident})
    print(f'Сообщение: {message}\n')

    # P подписывает это сообщение своим секретным ключом
    print('P подписывает это сообщение своим секретным ключом')
    # P -> signature = cert(rp,rv,Vid)
    signature = rsa.sign(message.encode(), p.private_key, HASHING_ALGORYTHM)
    print(f'Подпись: {signature}\n')

    # P передает подпись и своё случайное число
    print('P передает подпись и своё случайное число')
    # P (signature) -> V
    # P (rp) -> V

    # V составляет сообщение, которое должно было быть подписано P
    print('V составляет сообщение, которое должно было быть подписано P')
    message_to_verify = json.dumps({"rv": rv,
                                    "rp": rp,
                                    "Vid": v.ident})
    print(f'Составленное сообщение, подпись которого, нужно проверить: {message_to_verify}\n')

    # V проверяет составленное сообщение своим закрытым ключом
    print('V проверяет составленное сообщение своим закрытым ключом')
    hashing_algorythm = rsa.verify(message_to_verify.encode(), signature, v.public_key)

    if hashing_algorythm == HASHING_ALGORYTHM:
        print('Проверка проведена успешно')
