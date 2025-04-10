import random
import string

from typing_extensions import LiteralString


def get_random_string(length: int, symbols: list | tuple | set | str = None) -> string:
    """
    Generate a random string of given length with specified symbols

    :param length: Length of the generated string
    :param symbols: List of allowed symbols ['ascii_letters', 'digits', 'punctuation']
    (default is all printable ASCII characters)
    :return: A random string of specified length
    """

    if isinstance(symbols, str):
        symbols = (symbols,)

    _symbols: LiteralString = ''
    if 'ascii_letters' in symbols:
        _symbols = _symbols + string.ascii_letters
    if 'digits' in symbols:
        _symbols = _symbols + string.digits
    if 'punctuation' in symbols:
        _symbols += _symbols + string.punctuation
    if _symbols == '':
        _symbols = string.printable

    return ''.join(random.choice(_symbols) for _ in range(length))
