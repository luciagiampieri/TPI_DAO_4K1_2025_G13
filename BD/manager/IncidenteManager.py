import pymysql
from datetime import datetime

from BACK.modelos.Incidente import Incidente
from ..db_conection import DBConnection
from .TipoIncidenteManager import TipoIncidenteManager
# from .AlquilerManager import AlquilerManager  # Activar cuando lo quieras usar


class IncidenteManager:
    """Manager para la persistencia de objetos Incidente."""

    def __init__(self):
        self.db_connection = DBConnection()
        self.tipo_incidente_manager = TipoIncidenteManager()
        # self.alquiler_manager = AlquilerManager()  # para cuando quieras resolver la dependencia

    # ----------------------------------------------------------
    #   MAPEO FILA → OBJETO
    # ----------------------------------------------------------
    def __row_to_incidente(self, row):
        if row is None:
            return None

        tipo_incidente_obj = self.tipo_incidente_manager.obtener_por_id(row["ID_TIPO_INCIDENTE"])

        # TEMPORAL: Alquiler solo como ID hasta que lo conectes con AlquilerManager
        alquiler_obj = row["ID_ALQUILER"]

        fec_incidente = (row["FEC_INCIDENTE"]
            if row["FEC_INCIDENTE"]
            else None
        )

        return Incidente(
            id_incidente=row["ID_INCIDENTE"],
            tipo_incidente=tipo_incidente_obj,
            alquiler=alquiler_obj,
            fecha_incidente=fec_incidente,
            descripcion=row["DESCRIPCION"],
        )

    # ----------------------------------------------------------
    #   INSERTAR
    # ----------------------------------------------------------
    def guardar(self, incidente):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
                INSERT INTO INCIDENTE (ID_TIPO_INCIDENTE, ID_ALQUILER, FEC_INCIDENTE, DESCRIPCION) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                incidente.tipo_incidente.id_tipo_incidente,
                incidente.alquiler.id_alquiler, # Accedemos al ID del objeto Alquiler
                incidente.fecha_incidente,
                incidente.descripcion,
            ))
            conn.commit()
            incidente.id_incidente = cursor.lastrowid
            return incidente
        except Exception as e:
            print(f"Error al guardar incidente: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   OBTENER POR ID
    # ----------------------------------------------------------
    def obtener_por_id(self, id_incidente):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * 
                FROM INCIDENTE 
                WHERE ID_INCIDENTE = %s
            """, (id_incidente,))

            row = cursor.fetchone()
            return self.__row_to_incidente(row)

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
            cursor.execute("SELECT * FROM INCIDENTE")
            rows = cursor.fetchall()
            return [self.__row_to_incidente(row) for row in rows]

        finally:
            cursor.close()
            conn.close()

    def listar_por_alquiler(self, id_alquiler):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * 
                FROM INCIDENTE 
                WHERE ID_ALQUILER = %s
            """, (id_alquiler,))

            rows = cursor.fetchall()
            return [self.__row_to_incidente(row) for row in rows]

        finally:
            cursor.close()
            conn.close()

    def eliminar(self, id_incidente):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                DELETE FROM INCIDENTE 
                WHERE ID_INCIDENTE = %s
            """, (id_incidente,))

            conn.commit()
            return cursor.rowcount > 0

        except pymysql.MySQLError as e:
            print(f"Error al eliminar incidente: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

