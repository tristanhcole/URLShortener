import pytest
from utils import *


def test_decode():
    assert decode('B') == 1
    assert decode('g9dD92') == 30224534000

    with pytest.raises(TypeError):
        assert decode(1)


def test_encode():
    assert encode(1) == 'B'
    assert encode(30224534000) == 'g9dD92'

    with pytest.raises(TypeError):
        assert encode('B')


def test_validate_slug():
    assert validate_slug(None) is None
    assert validate_slug('asdf') == 'asdf'

    with pytest.raises(InvalidSlug):
        validate_slug('!')


def test_validate_dest():
    assert validate_dest('google.com') == 'https://google.com'
    assert validate_dest('https://google.com') == 'https://google.com'

    with pytest.raises(InvalidDest):
        assert validate_dest('goo')
        assert validate_dest('goo .com')
        assert validate_dest(None)