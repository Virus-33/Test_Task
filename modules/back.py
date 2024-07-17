from modules import DB_Access
from modules import security
from models import User

# I planned to make a Facade here, but something went wrong


def check_user(login: str, password: str) -> User:
    """
    Check user in database by login and password.
    :param login: user's login as str
    :param password: user's salted and hashed password as str
    :return: None if user not found, User object if login and password are correct
    """
    salt = DB_Access.check(login)
    if salt == '-100':
        return None
    password += salt
    password = security.get_hash(password)
    user = DB_Access.log(login, password)
    return user


def register(login: str, password: str):
    """
    Salts and hashes user's password, then adds user in database.
    :param login: user's login
    :param password: user's raw password
    """""
    salt = security.salt_gen()
    password += salt
    password = security.get_hash(password)
    DB_Access.add_user(login, password, salt)
