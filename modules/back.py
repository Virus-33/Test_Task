from modules import DB_Access
from modules import security


def check_user(login: str, password: str):
    salt = DB_Access.check(login)
    if salt == '-100':
        return None
    print(salt)
    password += salt
    password = security.get_hash(password)
    user = DB_Access.log(login, password)
    return user


def register(login: str, password: str):
    salt = security.salt_gen()
    password += salt
    password = security.get_hash(password)
    DB_Access.add_user(login, password, salt)
