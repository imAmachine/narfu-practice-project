from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, login, password):
        self.id = user_id
        self.login = login
        self.password = password

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False