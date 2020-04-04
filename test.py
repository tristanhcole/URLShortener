import timeit

current_random_slug_id = 0

BASE62 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def decode(string, base=BASE62):
    """
    Decode any string to integer.
    :param string: unique string to decode
    :param base: base to decode from
    :return: original unique  integer
    """
    base_len = len(base)

    num = 0
    for i, c in enumerate(string[::-1]):
        num += (base_len ** i) * base.find(c)
    return num


def encode(num, base=BASE62):
    """
    Encode any integer to any base string. Generates a unique random slug.
    :param num: unique random integer
    :param base: BASE to encode to
    :return: unique random slug
    """
    base_len = len(base)
    if num < base_len:
        return base[num]
    else:
        return encode(num // base_len, base) + base[num % base_len]


def generate_random_slug():
    global current_random_slug_id
    new_slug = encode(current_random_slug_id)
    current_random_slug_id += 1
    print(new_slug, current_random_slug_id)
    return new_slug


if __name__ == "__main__":
    start = timeit.default_timer()

    for x in range(10000):
        generate_random_slug()

    stop = timeit.default_timer()

    print('Time: ', stop - start)
