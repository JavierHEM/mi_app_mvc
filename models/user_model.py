import bcrypt
from config.database import DatabaseConnection

class UserModel:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def authenticate_user(self, username, password):
        """Autenticar usuario con username y contraseña"""
        try:
            connection = self.db.connect()
            if not connection:
                return None
            
            # Buscar usuario por username o email
            query = """
                SELECT u.*, r.name as role_name
                FROM users u
                LEFT JOIN r ON u.role_id = r.id
                WHERE (u.username = %s OR u.email = %s) AND u.is_active = TRUE
            """
            result = self.db.fetch_query(query, (username, username))

            if result and len(result > 0):
                user = result[0]

                # Verificar contraseña
                if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                    #Actualizar ultio login
                    self.update_last_login(user['id'])
                    return user
                
                return None
            
        except Exception as e:
            print(f"Error en autenticacion: {e}")
            return None
        finally:
            self.db.disconnect()
    
    def update_last_login(self, user_id):
        """Actualizar la fecha del ultimo login"""
        try:
            connection = self.db.connect()
            if connection:
                query = "UPDATE users SET last_login = NOW() WHERE id = %s"
                self.db.execute_query(query, (user_id,))
        except Exception as e:
            print(f"Error actualizando ultimo login {e}")
    
    def get_user_by_id(self, user_id):
        """Obtener usuario por ID"""
        try:
            connection = self.db.connect()
            if not connection:
                return None
            
            query = """
                SELECT u.*, r.name as role_name
                FROM users u
                LEFT JOIN roles r ON u.role_id = r.id
                WHERE u.id = %s AND u.is_active = TRUE
            """
            result = self.db.fetch_query(query, (user_id))

            if result and len(result) > 0:
                return result[0]
            return None
        except Exception as e:
            print(f"Error obteniendo usuario: {e}")
            return None
        finally:
            self.db.disconnect()