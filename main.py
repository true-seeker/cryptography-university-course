import random
import string


def trigram_generator(text):
    trigram = '  '
    for i in text:
        trigram += i
        yield trigram
        trigram = trigram[1:]


def calculate_text_index(text_prb, lang_trigrams):
    xi = 0
    for i in text_prb:
        xi += lang_trigrams[i] * text_prb[i]
    return xi


def generate_random_key():
    a = list(string.ascii_lowercase)
    random.shuffle(a)
    return a


def calculate_text_probabilities(text, trigram_dict):
    trigram_dict = {i: 0 for i in trigram_dict}
    trigram_count = 0

    for trigram in trigram_generator(text):
        if trigram in trigram_dict:
            trigram_dict[trigram] += 1
            trigram_count += 1
    trigram_probabilities = {key: value / trigram_count for key, value in zip(trigram_dict, trigram_dict.values())}
    return trigram_probabilities


def map_key(key: list) -> dict:
    mapped_key = {}
    for i, j in zip(string.ascii_lowercase, key):
        mapped_key[j] = i

    return mapped_key


def decrypt_text(text: str, key: list) -> str:
    decrypted = ''
    key = map_key(key)
    # for trigram in trigram_generator(text):
    #     trigram_part = trigram[-1]
    #     decrypted_trigram = ''
    #     if trigram_part in key:
    #         decrypted_trigram += key[trigram_part]
    #     else:
    #         decrypted_trigram += trigram_part
    #
    #     decrypted += decrypted_trigram
    for i in text:
        if i in key:
            decrypted += key[i]
        else:
            decrypted += i
    return decrypted


def mutate_key(key: list) -> list:
    pos_a = random.randint(0, len(key) - 1)
    pos_b = random.randint(0, len(key) - 1)
    if pos_a == pos_b:
        return mutate_key(key)

    key[pos_a], key[pos_b] = key[pos_b], key[pos_a]

    return key


def load_trigrams():
    trigrams = {}
    with open('trigrams_freq', 'r') as f:
        for line in f:
            line = line.split()
            trigrams[line[0].lower()] = int(line[1])
    s = sum(i for i in trigrams.values())

    for i in trigrams:
        trigrams[i] = trigrams[i] / s

    return trigrams


if __name__ == '__main__':
    text = ''
    with open('text.txt', 'r') as f:
        for i in f:
            text += i.lower()
    trigrams_dict = load_trigrams()
    test_key = 'vbcxznmlkjhgfdsawqertyuiop'
    decrypt_test = decrypt_text(text, test_key)
    test_prob = calculate_text_probabilities(decrypt_test, trigrams_dict)
    test_xi = calculate_text_index(test_prob, trigrams_dict)
    print(test_xi)
    # print(decrypt_test)
    # quit()

    current_xi = 0
    max_xi = current_xi

    saved_key = None
    random_key = generate_random_key()
    # random_key = [i for i in test_key]
    k = 0
    success_k = 0
    while True:
        k += 1
        if k - success_k > 500:
            random_key = mutate_key(random_key)
        else:
            random_key = generate_random_key()

        decrypted_text = decrypt_text(text, random_key)
        text_probabilities = calculate_text_probabilities(decrypted_text, trigrams_dict)
        current_xi = calculate_text_index(text_probabilities, trigrams_dict)
        if current_xi > max_xi:
            print(k, current_xi, random_key, decrypted_text[0:100])
            saved_key = list(random_key)
            max_xi = current_xi
            success_k = k

    print(saved_key)
    print(decrypt_text(text, saved_key)[0:100])
