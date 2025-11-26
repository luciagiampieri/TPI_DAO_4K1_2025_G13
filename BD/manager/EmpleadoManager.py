import mysql.connector
from BACK.modelos.Empleado import Empleado
from ..db_conection import DBConnection


class EmpleadoManager:
    """Manager para manejar la persistencia de objetos Empleado (ABM)."""
    
    def __init__(self):
        self.db_connection = DBConnection()

    # ----------------------------------------------------------
    # MAPEADOR FILA → OBJETO
    # ----------------------------------------------------------
    def __row_to_empleado(self, row):
        if row is None:
            return None

        return Empleado(
            id_empleado=row['ID_EMPLEADO'],
            nombre=row['NOMBRE'],
            dni=row['DNI'],
            mail=row['MAIL']
        )

    # ----------------------------------------------------------
    # CREAR
    # ----------------------------------------------------------
    def guardar(self, empleado):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO EMPLEADO (NOMBRE, DNI, MAIL) 
                VALUES (%s, %s, %s)
            """, (empleado.nombre, empleado.dni, empleado.mail))

            empleado.id_empleado = cursor.lastrowid
            conn.commit()
            return empleado

        except mysql.connector.Error as e:
            print(f"Error al guardar el empleado: {e}")
            conn.rollback()
            return None

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    # OBTENER POR ID
    # ----------------------------------------------------------
    def obtener_por_id(self, id_empleado):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT * 
                FROM EMPLEADO 
                WHERE ID_EMPLEADO = %s
            """, (id_empleado,))

            row = cursor.fetchone()
            return self.__row_to_empleado(row)

        except mysql.connector.Error as e:
            print(f"Error al obtener empleado: {e}")
            return None

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    # LISTAR TODOS
    # ----------------------------------------------------------
    def listar_todos(self):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM EMPLEADO")
            rows = cursor.fetchall()
            return [self.__row_to_empleado(row) for row in rows]

        except mysql.connector.Error as e:
            print(f"Error al listar empleados: {e}")
            return []

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    # ACTUALIZAR
    # ----------------------------------------------------------
    def actualizar(self, empleado):
        if not empleado.id_empleado:
            print("Error: No se puede actualizar un empleado sin ID.")
            return False

        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE EMPLEADO
                SET NOMBRE = %s, DNI = %s, MAIL = %s
                WHERE ID_EMPLEADO = %s
            """, (empleado.nombre, empleado.dni, empleado.mail, empleado.id_empleado))

            conn.commit()
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"Error al actualizar empleado: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    # ELIMINAR
    # ----------------------------------------------------------
    def eliminar(self, id_empleado):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                DELETE FROM EMPLEADO
                WHERE ID_EMPLEADO = %s
            """, (id_empleado,))

            conn.commit()
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"Error al eliminar empleado: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()
