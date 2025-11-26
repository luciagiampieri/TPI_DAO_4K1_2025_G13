import pymysql
from BACK.modelos.TipoMantenimiento import TipoMantenimiento
from ..db_conection import DBConnection


class TipoMantenimientoManager:
    """Manager para manejar la persistencia de objetos TipoMantenimiento."""

    def __init__(self):
        self.db_connection = DBConnection()

    # ----------------------------------------------------------
    #   MAPEAR FILA → OBJETO
    # ----------------------------------------------------------
    def __row_to_tipo_mantenimiento(self, row):
        if row is None:
            return None

        return TipoMantenimiento(
            id_tipo_mantenimiento=row["ID_TIPO_MANTENIMIENTO"],
            tipo_mantenimiento=row["TX_TIPO_MANTENIMIENTO"]
        )

    # ----------------------------------------------------------
    #   OBTENER POR ID
    # ----------------------------------------------------------
    def obtener_por_id(self, id_tipo_mantenimiento):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * 
                FROM TIPO_MANTENIMIENTO 
                WHERE ID_TIPO_MANTENIMIENTO = %s
            """, (id_tipo_mantenimiento,))

            row = cursor.fetchone()
            return self.__row_to_tipo_mantenimiento(row)

        except pymysql.MySQLError as e:
            print(f"Error al obtener tipo de mantenimiento: {e}")
            return None
        
        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   LISTAR TODOS
    # ----------------------------------------------------------
    def listar_todos(self):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM TIPO_MANTENIMIENTO")
            rows = cursor.fetchall()
            return [self.__row_to_tipo_mantenimiento(row) for row in rows]

        except pymysql.MySQLError as e:
            print(f"Error al listar tipos de mantenimiento: {e}")
            return []

        finally:
            cursor.close()
            conn.close()
