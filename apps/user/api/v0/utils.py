import random
import string


def generate_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choices(characters, k=6))
    return code
