import mysql.connector
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

        fec_incidente = (
            datetime.strptime(row["FEC_INCIDENTE"], "%Y-%m-%d %H:%M:%S")
            if row["FEC_INCIDENTE"]
            else None
        )

        return Incidente(
            id_incidente=row["ID_INCIDENTE"],
            tipo_incidente=tipo_incidente_obj,
            alquiler=alquiler_obj,
            fecha_incidente=fec_incidente,
            descripcion=row["DESCRIPCION"],
            costo=row["COSTO"]
        )

    # ----------------------------------------------------------
    #   INSERTAR
    # ----------------------------------------------------------
    def guardar(self, incidente):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            fec_incidente_str = incidente.fecha_incidente.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO INCIDENTE 
                    (ID_TIPO_INCIDENTE, ID_ALQUILER, FEC_INCIDENTE, DESCRIPCION, COSTO)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                incidente.tipo_incidente.id_tipo_incidente,
                incidente.alquiler,        # ya que estás usando ID directamente
                fec_incidente_str,
                incidente.descripcion,
                incidente.costo
            ))

            incidente.id_incidente = cursor.lastrowid
            conn.commit()
            return incidente

        except mysql.connector.Error as e:
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
        cursor = conn.cursor(dictionary=True)

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
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM INCIDENTE")
            rows = cursor.fetchall()
            return [self.__row_to_incidente(row) for row in rows]

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   ACTUALIZAR
    # ----------------------------------------------------------
    def actualizar(self, incidente):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            fec_incidente_str = incidente.fecha_incidente.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                UPDATE INCIDENTE 
                SET ID_TIPO_INCIDENTE = %s,
                    ID_ALQUILER = %s,
                    FEC_INCIDENTE = %s,
                    DESCRIPCION = %s,
                    COSTO = %s
                WHERE ID_INCIDENTE = %s
            """, (
                incidente.tipo_incidente.id_tipo_incidente,
                incidente.alquiler,
                fec_incidente_str,
                incidente.descripcion,
                incidente.costo,
                incidente.id_incidente
            ))

            conn.commit()
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"Error al actualizar incidente: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()
