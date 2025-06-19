import bcrypt
from config.database import DatabaseConnection

class UserModel:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def authenticate_user(self, username, password):
        """Autenticar usuario con username y contraseña"""