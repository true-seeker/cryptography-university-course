from utilities import convert_python_bin, middle_string_swap, xor

WORD_LENGTH = 16
KEY_LENGTH = 16
ROUND_KEY_LENGTH = 8
BLOCK_SIZE = 2
ITERATION_COUNT = 4
EMPTY_SYMBOL_PLACEHOLDER = ' '
ALPHABET = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, ' ': 10}


def encrypt_message(message: str, key: str) -> str:
    binary_key = ''.join([convert_python_bin(bin(ALPHABET[i])) for i in key])
    print('binary_key', binary_key)
    round_keys_list = [binary_key[:8], binary_key[3:11], binary_key[6:14], binary_key[8:16]]
    encrypted_message = ''
    blocks_list = [message[i:i + BLOCK_SIZE] for i in range(0, len(message), BLOCK_SIZE)]
    if len(blocks_list[-1]) == 1:
        blocks_list[-1] += EMPTY_SYMBOL_PLACEHOLDER

    for block in blocks_list:
        print('block', block)
        k = 0
        first_letter_id = ALPHABET[block[0]]
        second_letter_id = ALPHABET[block[1]]
        first_letter_binary_id = convert_python_bin(bin(first_letter_id))
        second_letter_binary_id = convert_python_bin(bin(second_letter_id))

        for i in range(ITERATION_COUNT):
            first_letter_binary_id = xor(first_letter_binary_id, round_keys_list[k])
            second_letter_binary_id = middle_string_swap(second_letter_binary_id)

            first_letter_binary_id, second_letter_binary_id = second_letter_binary_id, first_letter_binary_id
            k += 1
        encrypted_message += f'{chr(int(first_letter_binary_id, 2))}{chr(int(second_letter_binary_id, 2))}'

    print(f'message: {message}')
    print(f'encrypted_message: {encrypted_message}')
    return encrypted_message


if __name__ == '__main__':
    input_message = '1337'
    input_key = '25'
    encrypted = encrypt_message(input_message, input_key)
