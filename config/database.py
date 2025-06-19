import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'mi_app_db'
        self.user = 'user_app'
        self.password = 'Admin123!'
        self.conecction = None

    def connect(self):
        """Establecer conexion con la base de datos"""

        try: 
            self.connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password
            )

            if self.conecction.is_connected():
                print("Conexion exitosa a MySQL")
                return self.conecction
        except Error as e:
            print(f"Error al conectar con MySQL: {e}")
            return None
        
    def disconnect(self):
        """Cerrar conexion con la base de datos"""
        if self.conecction and self.conecction.is_connected():
            self.conecction.close()
            print("Conexion cerrada")

    def execute_query(self, query, params=None):
        """Ejecutar connsulta que no retorna datos (INNSERT, UPDATE, DELETE)"""
        try:
            cursor = self.conecction.cursor()
            cursor.execute(query, params)
            self.conecction.commit()
            result = cursor.rocount
            cursor.close()
            return result
        except Error as e:
            print(f"Error ejecutando consulta: {e}")
            return None
        
    def fetch_query(self, query, params=None):
        """Ejecutar consulta que retorna datos (SELECT)"""
        try:
            cursor = self.conecction.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error en consulta: {e}")
            return None