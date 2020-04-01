import timeit

current_random_slug_id = 0


def base_conversion(n, base=62):
    """
    Convert integer to base62 slug to generate unique random slug
    :param n:
    :param base:
    :return:
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    if n < base:
        return alphabet[n]
    else:
        return base_conversion(n//base, base) + alphabet[n%base]


def generate_random_slug():
    global current_random_slug_id
    new_slug = base_conversion(current_random_slug_id)
    current_random_slug_id += 1
    print(new_slug, current_random_slug_id)
    return new_slug


if __name__ == "__main__":
    start = timeit.default_timer()

    for x in range(100000):
        generate_random_slug()

    stop = timeit.default_timer()
    print('Time: ', stop - start)
