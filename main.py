import random
import string

natural_language_probabilities = {
    'e': 0.12702,
    't': 0.09356,
    'a': 0.08167,
    'o': 0.07507,
    'i': 0.06966,
    'n': 0.06749,
    's': 0.06327,
    'h': 0.06094,
    'r': 0.05987,
    'd': 0.04253,
    'l': 0.04025,
    'u': 0.02758,
    'w': 0.02560,
    'm': 0.02406,
    'f': 0.02228,
    'c': 0.02202,
    'g': 0.02015,
    'y': 0.01994,
    'p': 0.01929,
    'b': 0.01492,
    'k': 0.01292,
    'v': 0.00978,
    'j': 0.00153,
    'x': 0.00150,
    'q': 0.00095,
    'z': 0.00077
}


def calculate_text_index(text, f):
    xi = 0
    for i in text:
        if i not in natural_language_probabilities:
            continue
        xi += natural_language_probabilities[i] * f[i]
    return xi


def generate_random_key():
    a = list(string.ascii_lowercase)
    random.shuffle(a)
    return ''.join(a)


def calculate_text_probabilities(text):
    letter_count = {}
    text_length = len(text)
    for i in text:
        if i not in natural_language_probabilities:
            text_length -= 1
            continue
        if letter_count.get(i) is None:
            letter_count[i] = 1
        else:
            letter_count[i] += 1
    letter_probabilities = {key: value / text_length for key, value in zip(letter_count, letter_count.values())}

    return letter_probabilities


def map_key(key: str):
    mapped_key = {}
    for i, j in zip(string.ascii_lowercase, key):
        mapped_key[i] = j

    return mapped_key


def decrypt_text(text, key):
    decrypted = ''
    key = map_key(key)
    for i in text:
        if i in key:
            decrypted += key[i]
        else:
            decrypted += i
    return decrypted


if __name__ == '__main__':
    text = ''
    with open('text.txt', 'r') as f:
        for i in f:
            text += i.lower()

    max_xi = 0
    current_xi = 0.01
    saved_key = None
    while True:
        random_key = generate_random_key()
        decrypted_text = decrypt_text(text, random_key)
        text_probabilities = calculate_text_probabilities(decrypted_text)
        current_xi = calculate_text_index(decrypted_text, text_probabilities)
        if current_xi > max_xi:
            max_xi = current_xi
            saved_key = random_key
            print(max_xi, saved_key)
            print(decrypted_text[0:100])
        elif current_xi == max_xi:
            break

    print(saved_key)
