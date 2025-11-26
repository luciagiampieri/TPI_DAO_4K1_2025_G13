import mysql.connector
from mysql.connector import errorcode

class DBConnection:
    
    def __init__(self):
        # Configuración de tu servidor MySQL local
        self.config = {
            'user': 'root',  # Ejemplo: 'root' o el que creaste
            'password': 'root123',
            'host': '127.0.0.1',
            'database': 'alquiler_autos' # Nombre de la BD que creaste en MySQL
        }

    def get_connection(self):
        """Retorna una conexión activa a la base de datos MySQL."""
        try:
            conn = mysql.connector.connect(
                **self.config,
                cursor_class=mysql.connector.cursor.MySQLCursorDict
                )
            return conn
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Usuario o contraseña incorrectos.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Error: La base de datos no existe.")
            else:
                print(f"Error de conexión a MySQL: {err}")
            return None

    def execute_sql_script(self, sql_script):
        """Ejecuta un script DDL para crear tablas (usa este método para crear el esquema)."""
        conn = self.get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # El método multi=True permite ejecutar múltiples sentencias CREATE TABLE
                for result in cursor.execute(sql_script, multi=True):
                    if result.with_rows:
                        # Si hay resultados (SELECT), podrías procesarlos aquí
                        pass
                conn.commit()
                print("Esquema MySQL creado/actualizado correctamente.")
            except mysql.connector.Error as err:
                print(f"Error al ejecutar script SQL: {err}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

# Si quieres usar el archivo SQL que ya generamos, puedes cargarlo aquí
if __name__ == '__main__':
    # # Ruta por defecto al archivo .sql ubicado junto a este script
    # sql_file = os.path.join(os.path.dirname(__file__), 'schema.sql')

    # if not os.path.exists(sql_file):
    #     print(f"No se encontró el archivo SQL en: {sql_file}. Coloca tu archivo 'schema.sql' junto a este script o cambia la ruta.")
    # else:
    #     try:
    #         with open(sql_file, 'r', encoding='utf-8') as f:
    #             contenido_sql = f.read()
    #         db = DBConnection()
    #         db.execute_sql_script(contenido_sql)
    #     except Exception as e:
    #         print(f"Error al leer/ejecutar el archivo SQL: {e}")
    pass