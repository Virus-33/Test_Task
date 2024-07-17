from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, _id, login):
        self.id = _id
        self.login = login

