from ..models.user_model import UserModel
from ..utils.helpers import SecurityUtils

class AuthService:
    def __init__(self):
        self.user_model = UserModel()
        self.current_user = None

    def register(self, username, email, password):
        if self.user_model.get_user_by_username(username):
            return False, "Username already exists."
        if self.user_model.get_user_by_email(email):
            return False, "Email already exists."
        
        hashed_pw = SecurityUtils.hash_password(password)
        if self.user_model.create_user(username, email, hashed_pw):
            return True, "Registration successful."
        return False, "Registration failed."

    def login(self, username, password):
        user = self.user_model.get_user_by_username(username)
        if user and SecurityUtils.check_password(password, user['password_hash']):
            self.current_user = user
            return True, user
        return False, "Invalid username or password."

    def logout(self):
        self.current_user = None

    def is_admin(self):
        return self.current_user and self.current_user['role'] == 'admin'
