import pymysql
from BACK.modelos.Estado import Estado
from ..db_conection import DBConnection
from .AmbitoManager import AmbitoManager


class EstadoManager:
    """Manager para manejar la persistencia de objetos Estado."""

    def __init__(self):
        self.db_connection = DBConnection()
        self.ambito_dao = AmbitoManager()

    # ----------------------------------------------------------
    #   MAPEO FILA → OBJETO
    # ----------------------------------------------------------
    def __row_to_estado(self, row):
        if row is None:
            return None

        # Resolver la dependencia: Ambito
        ambito_obj = self.ambito_dao.obtener_por_id(row['ID_AMBITO'])

        return Estado(
            id_estado=row['ID_ESTADO'],
            estado=row['TX_ESTADO'],
            ambito=ambito_obj
        )

    # ----------------------------------------------------------
    #   OBTENER POR ID
    # ----------------------------------------------------------
    def obtener_por_id(self, id_estado):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT ID_ESTADO, TX_ESTADO, ID_AMBITO
                FROM ESTADO
                WHERE ID_ESTADO = %s
            """, (id_estado,))

            row = cursor.fetchone()
            return self.__row_to_estado(row)

        except pymysql.MySQLError as e:
            print(f"Error al obtener estado: {e}")
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
                SELECT ID_ESTADO, TX_ESTADO, ID_AMBITO
                FROM ESTADO
            """)

            rows = cursor.fetchall()
            return [self.__row_to_estado(row) for row in rows]

        except pymysql.MySQLError as e:
            print(f"Error al listar estados: {e}")
            return []

        finally:
            cursor.close()
            conn.close()

    def listar_por_ambito(self, ambito_id):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT ID_ESTADO, TX_ESTADO, ID_AMBITO
                FROM ESTADO
                WHERE ID_AMBITO = %s
            """, (ambito_id,))

            rows = cursor.fetchall()
            return [self.__row_to_estado(row) for row in rows]

        except pymysql.MySQLError as e:
            print(f"Error al listar estados por ámbito: {e}")
            return []

        finally:
            cursor.close()
            conn.close()
