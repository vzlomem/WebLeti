from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Простая модель пользователя
class User(UserMixin):
    def __init__(self, username):
        self.id = username  # id для Flask-Login
        self.username = username

    def check_password(self, password):
        stored_hash = users.get(self.username)
        if stored_hash:
            return check_password_hash(stored_hash, password)
        return False


# Словарь "пользователь: хэш_пароля"
users = {
    "admin": generate_password_hash("admin123"),
    "user": generate_password_hash("user123")
}
