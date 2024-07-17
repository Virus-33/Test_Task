from flask_login import UserMixin


# User class for Flask_Login
class User(UserMixin):

    def __init__(self, _id, login):
        self.id = _id
        self.login = login

