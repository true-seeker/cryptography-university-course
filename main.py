import json
import time

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

L = 1000

if __name__ == '__main__':
    a = 10
    b = 666
    k = [50, 213, 134, 119, 106, 169, 171, 107, 3, 131, 201, 128, 88, 237, 165, 140, 254, 184, 68, 39, 226, 253, 172,
         15, 154, 239, 135, 175, 254, 66, 56, 199]

    ka = [64, 51, 224, 165, 212, 77, 184, 85, 207, 173, 51, 127, 250, 197, 52, 239, 9, 141, 12, 20, 54, 201, 240, 148,
          176, 155, 214, 185, 91, 196, 43, 110]

    kb = [179, 35, 138, 70, 236, 57, 41, 238, 202, 117, 236, 140, 127, 210, 171, 125, 245, 181, 134, 173, 119, 204, 218,
          90, 53, 211, 86, 95, 240, 27, 185, 214]
    iv = bytes([0 for i in range(16)])

    tt = int(time.time())

    payload_a = {'Tt': tt,
                 'L': L,
                 'k': k,
                 'B': b}
    payload_b = {'Tt': tt,
                 'L': L,
                 'k': k,
                 'A': a}

    payload_a_str = json.dumps(payload_a)
    payload_a_str = str(payload_a_str) + ' ' * (16 - len(str(payload_a_str)) % 16)
    cipher_a = Cipher(algorithms.AES(bytes(ka)), modes.CBC(iv), backend=default_backend())
    decryptor_a = cipher_a.decryptor()
    encryptor_a = cipher_a.encryptor()
    ct_a = encryptor_a.update(str(payload_a_str).encode()) + encryptor_a.finalize()

    payload_b_str = json.dumps(payload_b)
    payload_b_str = str(payload_b_str) + ' ' * (16 - len(str(payload_b_str)) % 16)
    cipher_b = Cipher(algorithms.AES(bytes(kb)), modes.CBC(iv), backend=default_backend())
    decryptor_b = cipher_b.decryptor()
    encryptor_b = cipher_b.encryptor()
    ct_b = encryptor_b.update(str(payload_b_str).encode()) + encryptor_b.finalize()

    print("Часть Алисы:", list(ct_a))
    print("Часть Боба:", list(ct_b))
    print()

    decrypted_message_a_str = (decryptor_a.update(ct_a) + decryptor_a.finalize()).decode('utf-8')
    decrypted_message_b_str = (decryptor_b.update(ct_b) + decryptor_b.finalize()).decode('utf-8')

    decrypted_message_a = json.loads(decrypted_message_a_str)
    decrypted_message_b = json.loads(decrypted_message_b_str)

    print(decrypted_message_a)
    print(decrypted_message_b)
