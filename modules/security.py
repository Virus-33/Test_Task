import random
import hashlib


def salt_gen() -> str:
    """Generates random salt for password.
        For this task salt is always has a legth of 2 sybmols.
        Returns:
            Random salt as string"""
    result = ''
    a = random.randint(1, 99)
    b = random.randint(1, 99)
    result += chr(a) + chr(b)
    return result


def get_hash(pass_string: str) -> str:
    """Hashes user's password.
    Arguments:
        pass_string (str): User's salted password
    Returns:
        Hashed password as str"""
    pass_string = pass_string.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(pass_string)
    return str(hash_object.hexdigest())

