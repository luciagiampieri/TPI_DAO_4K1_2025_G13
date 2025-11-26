import pymysql
from BACK.modelos.Ambito import Ambito
from ..db_conection import DBConnection


class AmbitoManager:
    """Manager para manejar la persistencia de objetos Ambito en MySQL."""

    def __init__(self):
        self.db_connection = DBConnection()

    # ----------------------------------------------------------
    #   MAPEO FILA → OBJETO
    # ----------------------------------------------------------
    def __row_to_ambito(self, row):
        if row is None:
            return None

        return Ambito(
            id_ambito=row['ID_AMBITO'],
            ambito=row['TX_AMBITO']
        )

    # ----------------------------------------------------------
    #   OBTENER POR ID
    # ----------------------------------------------------------
    def obtener_por_id(self, id_ambito):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT ID_AMBITO, TX_AMBITO
                FROM AMBITO
                WHERE ID_AMBITO = %s
            """, (id_ambito,))

            row = cursor.fetchone()
            return self.__row_to_ambito(row)

        except pymysql.MySQLError as e:
            print(f"Error al obtener ámbito: {e}")
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
            cursor.execute("""
                SELECT ID_AMBITO, TX_AMBITO
                FROM AMBITO
            """)

            rows = cursor.fetchall()
            return [self.__row_to_ambito(row) for row in rows]

        except pymysql.MySQLError as e:
            print(f"Error al listar ámbitos: {e}")
            return []

        finally:
            cursor.close()
            conn.close()
