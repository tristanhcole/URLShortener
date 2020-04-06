import re
from server.exceptions import InvalidSlug, InvalidDest

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


def validate_slug(slug):
    """
    Validates slug is valid.
    :param slug: Must be part of BASE62 or SPECIAL_CHARS
    :return: slug or raise exception
    """
    if slug is None:
        return None
    regex = re.compile(r'[a-zA-Z0-9]+')
    if re.match(regex, slug) is not None:
        return slug
    else:
        raise InvalidSlug('Slug Provided is invalid')


def validate_dest(dest):
    """
    Validates dest are valid URLs.
    :param dest: google.com
    :return: dest or raise exception
    """
    if dest is None:
        raise InvalidDest('Destination URL provided must not be None')

    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, dest) is not None:
        return dest

    # try add scheme to dest
    new_dest = 'https://'+dest
    if re.match(regex, new_dest) is not None:
        return new_dest

    else:
        raise InvalidDest('Destination URL provided is invalid')
