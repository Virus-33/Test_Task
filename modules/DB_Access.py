import sqlite3
from models.User import User

# base strings with commands to database. Substitudes values with str.format() later
create = 'insert into Users (Login, Pass, Salt) values ("{0}", "{1}", "{2}")'
read = 'select Login from Users'
update = 'update Users set Pass="{0}" where ID="{1}"'
delete = 'delete from Users where ID="{0}"'

log_in = 'select ID from Users where Login="{0}" and Pass="{1}"'
user_check = 'select Salt from Users where Login="{0}"'
get = 'select Login from Users where ID = "{0}"'


def add_user(login: str, password: str, salt: str):
    """
    Creates new user in Users table.
    :param login: user's login
    :param password: user's salted and hashed password
    :param salt: salt for user's password
    """
    con = sqlite3.connect('bd/task.db')
    cursor = con.cursor()
    cursor.execute(str.format(create, login, password, salt))
    con.commit()
    cursor.close()


def get_users() -> list:
    """
    Read logins of all users.
    :return: A lot of logins
    """
    con = sqlite3.connect('bd/task.db')
    cursor = con.cursor()
    cursor.execute(read)
    result = cursor.fetchall()[0]
    cursor.close()
    return result


def update_password(user_id: int, new_pass: str):
    """
    Changes user's password in database.
    :param user_id: user's id in database
    :param new_pass: user's new password, hashed and salted
    """
    con = sqlite3.connect('bd/task.db')
    cursor = con.cursor()
    cursor.execute(str.format(update, user_id, new_pass))
    con.commit()
    cursor.close()


def delete_user(user_id: int):
    """
    Remove user from database by id.
    :param user_id: user's id in database
    """
    con = sqlite3.connect('bd/task.db')
    cursor = con.cursor()
    cursor.execute(str.format(delete, user_id))
    con.commit()
    cursor.close()


def log(login: str, password: str):
    """
    Get user's id if user exists and password is typed correctly.
    :param login: user's login
    :param password: salted and hashed password
    :return: User object on success, None on fail
    """
    con = sqlite3.connect('bd/task.db')
    cursor = con.cursor()
    cursor.execute(str.format(log_in, login, password))
    results = cursor.fetchall()
    if len(results) > 0:
        cursor.close()
        return User(results[0][0], login)
    cursor.close()
    return None


def check(login: str) -> str:
    """
    Get all users with this login, return '-100' if there is no such login or salt if login exists.
    :param login: user's login
    :return: User's salt for password
    """
    con = sqlite3.connect('bd/task.db')
    cursor = con.cursor()
    cursor.execute(str.format(user_check, login))
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.close()
        return '-100'
    cursor.close()
    return result[0][0]


def get_by_id(_id: int) -> User:
    """
    Get User as object. Necessary for login manager.
    :param _id: user's id
    :return: user object on success, None if no such user
    """
    con = sqlite3.connect('bd/task.db')
    cursor = con.cursor()
    cursor.execute(str.format(get, _id))
    results = cursor.fetchall()
    cursor.close()
    if len(results) > 0:
        return User(_id, results[0][0])
    return None
