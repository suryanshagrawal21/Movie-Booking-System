from ..models.user_model import UserModel
from ..utils.helpers import SecurityUtils
import re
import time

class AuthService:
    def __init__(self):
        self.user_model = UserModel()
        self.current_user = None
        self.session_start = None

    def valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def valid_password(self, password):
        return len(password) >= 6

    def register(self, username, email, password):
        if not self.valid_email(email):
            return False, "Invalid email format."
        if not self.valid_password(password):
            return False, "Password must be at least 6 characters."
            
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
        if not user:
            user = self.user_model.get_user_by_email(username)
            
        if user and SecurityUtils.check_password(password, user['password_hash']):
            self.current_user = user
            self.session_start = time.time()
            return True, user
        return False, "Invalid username or password."

    def is_session_valid(self):
        if not self.current_user or not self.session_start:
            return False
        return time.time() - self.session_start < 1800  # 30 min timeout

    def logout(self):
        self.current_user = None
        self.session_start = None

    def is_admin(self):
        return self.current_user and self.current_user['role'] == 'admin'
