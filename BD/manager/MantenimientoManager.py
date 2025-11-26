import pymysql
from datetime import datetime

from BACK.modelos.Mantenimiento import Mantenimiento
from ..db_conection import DBConnection
from .VehiculoManager import VehiculoManager 
from .TipoMantenimientoManager import TipoMantenimientoManager 


class MantenimientoManager:
    """Manager para manejar la persistencia de objetos Mantenimiento en MySQL."""
    
    def __init__(self):
        self.db_connection = DBConnection()
        self.vehiculo_manager = VehiculoManager()
        self.tipo_mantenimiento_manager = TipoMantenimientoManager()

    # ----------------------------------------------------------
    #   MAPEO FILA → OBJETO
    # ----------------------------------------------------------
    def __row_to_mantenimiento(self, row):
        if row is None:
            return None

        vehiculo_obj = self.vehiculo_manager.obtener_por_id(row["ID_VEHICULO"])
        tipo_mto_obj = self.tipo_mantenimiento_manager.obtener_por_id(row["ID_TIPO_MANTENIMIENTO"])

        fec_inicio = (
            datetime.strptime(row["FEC_INICIO"], "%Y-%m-%d %H:%M:%S")
            if row["FEC_INICIO"] else None
        )
        fec_fin = (
            datetime.strptime(row["FEC_FIN"], "%Y-%m-%d %H:%M:%S")
            if row["FEC_FIN"] else None
        )

        return Mantenimiento(
            id_mantenimiento=row["ID_MANTENIMIENTO"],
            vehiculo=vehiculo_obj,
            tipo_mantenimiento=tipo_mto_obj,
            fecha_inicio=fec_inicio,
            fecha_fin=fec_fin,
            costo=row["COSTO"],
            observacion=row["OBSERVACION"]
        )

    # ----------------------------------------------------------
    #   INSERTAR
    # ----------------------------------------------------------
    def guardar(self, mantenimiento):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            fec_inicio_str = mantenimiento.fecha_inicio.strftime("%Y-%m-%d %H:%M:%S")
            fec_fin_str = (
                mantenimiento.fecha_fin.strftime("%Y-%m-%d %H:%M:%S")
                if mantenimiento.fecha_fin else None
            )

            cursor.execute("""
                INSERT INTO MANTENIMIENTO 
                    (ID_VEHICULO, ID_TIPO_MANTENIMIENTO, FEC_INICIO, FEC_FIN, COSTO, OBSERVACION)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                mantenimiento.vehiculo.id_vehiculo,
                mantenimiento.tipo_mantenimiento.id_tipo_mantenimiento,
                fec_inicio_str,
                fec_fin_str,
                mantenimiento.costo,
                mantenimiento.observacion
            ))

            mantenimiento.id_mantenimiento = cursor.lastrowid
            conn.commit()
            return mantenimiento

        except pymysql.MySQLError as e:
            print(f"Error al guardar mantenimiento: {e}")
            conn.rollback()
            return None

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   OBTENER POR ID
    # ----------------------------------------------------------
    def obtener_por_id(self, id_mantenimiento):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * 
                FROM MANTENIMIENTO
                WHERE ID_MANTENIMIENTO = %s
            """, (id_mantenimiento,))

            row = cursor.fetchone()
            return self.__row_to_mantenimiento(row)

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   FINALIZAR MANTENIMIENTO (UPDATE)
    # ----------------------------------------------------------
    def finalizar_mantenimiento(self, id_mantenimiento, fecha_fin, costo):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            fec_fin_str = fecha_fin.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                UPDATE MANTENIMIENTO
                SET FEC_FIN = %s, COSTO = %s
                WHERE ID_MANTENIMIENTO = %s
            """, (fec_fin_str, costo, id_mantenimiento))

            conn.commit()
            return cursor.rowcount > 0

        except pymysql.MySQLError as e:
            print(f"Error al finalizar mantenimiento: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()
