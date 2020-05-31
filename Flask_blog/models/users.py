from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email):
        self.email = email

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return True

    @staticmethod
    def find_or_create_by_email(email):
        return User(email)

    @staticmethod
    def find_by_id(id):
        return User(id)
