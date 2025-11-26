import mysql.connector
from BACK.modelos.TipoIncidente import TipoIncidente
from ..db_conection import DBConnection


class TipoIncidenteManager:
    """Manager para manejar la persistencia de objetos TipoIncidente."""

    def __init__(self):
        self.db_connection = DBConnection()

    # ----------------------------------------------------------
    #   MAPEAR FILA → OBJETO
    # ----------------------------------------------------------
    def __row_to_tipo_incidente(self, row):
        if row is None:
            return None

        return TipoIncidente(
            id_tipo_incidente=row["ID_TIPO_INCIDENTE"],
            tipo_incidente=row["TX_INCIDENTE"]
        )

    # ----------------------------------------------------------
    #   OBTENER POR ID
    # ----------------------------------------------------------
    def obtener_por_id(self, id_tipo_incidente):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT * 
                FROM TIPO_INCIDENTE 
                WHERE ID_TIPO_INCIDENTE = %s
            """, (id_tipo_incidente,))

            row = cursor.fetchone()
            return self.__row_to_tipo_incidente(row)

        except mysql.connector.Error as e:
            print(f"Error al obtener tipo de incidente: {e}")
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
            cursor.execute("SELECT * FROM TIPO_INCIDENTE")
            rows = cursor.fetchall()
            return [self.__row_to_tipo_incidente(row) for row in rows]

        except mysql.connector.Error as e:
            print(f"Error al listar tipos de incidente: {e}")
            return []
        
        finally:
            cursor.close()
            conn.close()
