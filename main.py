from bitarray import bitarray
import PIL.Image as Image
from PIL import ImageFile
import io

ImageFile.LOAD_TRUNCATED_IMAGES = True

MAX_MESSAGE_SIZE = 10000
MESSAGE_LENGTH_SIZE = 32
BITS_OFFSET = 0


def encrypt(filename, output_filename, message):
    file_bits = bitarray()
    message_bits = bitarray()

    message_bits.frombytes(message.encode())
    assert len(message_bits) <= MAX_MESSAGE_SIZE

    message_length_bits = bitarray()
    message_length_bits.frombytes(str(len(message_bits)).encode())
    if len(message_length_bits) < MESSAGE_LENGTH_SIZE:
        message_length_bits = bitarray(MESSAGE_LENGTH_SIZE - len(message_length_bits)) + message_length_bits

    with open(filename, 'rb') as f:
        file_bits.fromfile(f)
    assert len(file_bits) >= len(message_bits) + len(message_length_bits)

    # запись длины сообщения
    for k, i in enumerate(message_length_bits):
        file_bits[len(file_bits) - 1 - (k * 8 + BITS_OFFSET)] = i

    # запись сообщения
    for k, i in enumerate(message_bits):
        file_bits[len(file_bits) - 1 - (len(message_length_bits) * 8 + k * 8 + BITS_OFFSET)] = i

    with open(output_filename, 'wb') as f:
        file_bits.tofile(f)


def decrypt(filename):
    file_bits = bitarray()
    message_bits = bitarray()
    message_length_bits = bitarray()

    with open(filename, 'rb') as f:
        file_bits.fromfile(f)

    # считывание длины сообщения
    for k in range(MESSAGE_LENGTH_SIZE):
        message_length_bits.append(file_bits[len(file_bits) - 1 - (k * 8 + BITS_OFFSET)])
    message_length = int(message_length_bits.tobytes().replace(b'\x00', b''))

    # считывание сообщения
    for k in range(message_length):
        message_bits.append(file_bits[len(file_bits) - 1 - (len(message_length_bits) * 8 + k * 8 + BITS_OFFSET)])

    return message_bits.tobytes().decode()


message = 'I HATE TERRAGROUP'
op_filename = 'encrypted.bmp'

encrypt('gosling.bmp', op_filename, message)

decrypted = decrypt(op_filename)
print(decrypted)
