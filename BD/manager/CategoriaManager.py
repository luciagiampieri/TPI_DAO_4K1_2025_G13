import mysql.connector
from BACK.modelos.Categoria import Categoria
from ..db_conection import DBConnection


class CategoriaManager:
    def __init__(self):
        self.db_connection = DBConnection()

    # ----------------------------------------------------------
    #   MAPEO FILA → OBJETO
    # ----------------------------------------------------------
    def __row_to_categoria(self, row):
        if row is None:
            return None

        return Categoria(
            id_categoria=row['ID_CATEGORIA'],
            categoria=row['TX_CATEGORIA']
        )

    # ----------------------------------------------------------
    #   OBTENER POR ID
    # ----------------------------------------------------------
    def obtener_por_id(self, id_categoria):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT ID_CATEGORIA, TX_CATEGORIA
                FROM CATEGORIA
                WHERE ID_CATEGORIA = %s
            """, (id_categoria,))

            row = cursor.fetchone()
            return self.__row_to_categoria(row)

        except mysql.connector.Error as e:
            print(f"Error al obtener categoría: {e}")
            return None

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   LISTAR TODOS
    # ----------------------------------------------------------
    def listar_todos(self):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT ID_CATEGORIA, TX_CATEGORIA
                FROM CATEGORIA
            """)

            rows = cursor.fetchall()
            return [self.__row_to_categoria(row) for row in rows]

        except mysql.connector.Error as e:
            print(f"Error al listar categorías: {e}")
            return []

        finally:
            cursor.close()
            conn.close()
