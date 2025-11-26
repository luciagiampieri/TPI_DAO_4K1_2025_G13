import pymysql
from BACK.modelos.Cliente import Cliente
from ..db_conection import DBConnection

class ClienteManager:
    """Clase Manager para manejar la persistencia de objetos Cliente."""

    def __init__(self):
        self.db_connection = DBConnection()

    # --- Función privada para mapear registros a objetos Cliente ---
    def __row_to_cliente(self, row):
        """Convierte un registro de la BD en un objeto Cliente."""
        if row is None:
            return None

        return Cliente(
            id_cliente=row['ID_CLIENTE'],
            nombre=row['NOMBRE'],
            dni=row['DNI'],
            telefono=row.get('TELEFONO'),
            mail=row.get('MAIL')
        )

    # --- 1. Crear (INSERT) ---
    def guardar(self, cliente):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO CLIENTE (NOMBRE, DNI, TELEFONO, MAIL)
                VALUES (%s, %s, %s, %s)
            """, (cliente.nombre, cliente.dni, cliente.telefono, cliente.mail))

            cliente.id_cliente = cursor.lastrowid
            conn.commit()
            return cliente

        except pymysql.err.IntegrityError:
            print(f"Error: Ya existe un cliente con el DNI {cliente.dni}.")
            return None

        except pymysql.MySQLError as e:
            print(f"Error al guardar el cliente: {e}")
            conn.rollback()
            return None

        finally:
            cursor.close()
            conn.close()

    # --- 2. Obtener por ID (SELECT) ---
    def obtener_por_id(self, id_cliente):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM CLIENTE WHERE ID_CLIENTE = %s", (id_cliente,))
            row = cursor.fetchone()
            return self.__row_to_cliente(row)

        except pymysql.MySQLError as e:
            print(f"Error al obtener cliente: {e}")
            return None

        finally:
            cursor.close()
            conn.close()

    # --- 3. Listar todos (SELECT *) ---
    def listar_todos(self):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM CLIENTE")
            rows = cursor.fetchall()
            return [self.__row_to_cliente(row) for row in rows]

        except pymysql.MySQLError as e:
            print(f"Error al listar clientes: {e}")
            return []

        finally:
            cursor.close()
            conn.close()

    # --- 4. Actualizar (UPDATE) ---
    def actualizar(self, cliente):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE CLIENTE 
                SET NOMBRE = %s, DNI = %s, TELEFONO = %s, MAIL = %s
                WHERE ID_CLIENTE = %s
            """, (cliente.nombre, cliente.dni, cliente.telefono, cliente.mail, cliente.id_cliente))

            conn.commit()
            return cursor.rowcount > 0  # True si modificó algo

        except pymysql.err.IntegrityError:
            print(f"Error: Ya existe un cliente con el DNI {cliente.dni}.")
            return False

        except pymysql.MySQLError as e:
            print(f"Error al actualizar el cliente: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()
