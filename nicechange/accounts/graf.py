import base64
import random
import string
def generate_random_string():
    """
    Returns a string with `length` characters chosen from `stringset`
    """
    return (base64.b32encode(bytes(''.join(random.choices(string.hexdigits, k=16)).encode()))).__str__()[2:18]


print(generate_random_string())