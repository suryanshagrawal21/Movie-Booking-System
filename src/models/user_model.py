from .base_model import BaseModel

class UserModel(BaseModel):
    def create_user(self, username, email, password_hash, role='user'):
        query = "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)"
        return self.execute_query(query, (username, email, password_hash, role))

    def get_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        return self.fetch_one(query, (username,))

    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email = %s"
        return self.fetch_one(query, (email,))

    def update_password(self, user_id, new_password_hash):
        query = "UPDATE users SET password_hash = %s WHERE id = %s"
        return self.execute_query(query, (new_password_hash, user_id))
