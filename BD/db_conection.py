import sqlite3

class DBConnection:
    """Clase para manejar la conexión a la base de datos SQLite."""
    # Nombre del archivo de la base de datos
    def __init__(self):
        self.DB_FILE = 'base.db'


    def get_connection(self):
        """Retorna una conexión a la base de datos."""
        # Esto creará el archivo DB_FILE si no existe, o se conectará a él.
        conn = sqlite3.connect(self.DB_FILE)
        # Habilitar el soporte para Foreign Keys (es crucial en SQLite)
        conn.execute("PRAGMA foreign_keys = ON") 
        return conn
