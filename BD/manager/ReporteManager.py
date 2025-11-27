# TPIDAO/BD/manager/ReporteManager.py
import pymysql
from ..db_conection import DBConnection

class ReporteManager:
    def __init__(self):
        self.db_connection = DBConnection()

    def obtener_ranking_vehiculos(self):
        """Top vehículos más alquilados."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        try:
            # Hacemos JOIN para mostrar Patente y Modelo, no solo IDs
            sql = """
                SELECT V.PATENTE, D.MODELO, COUNT(A.ID_ALQUILER) as CANTIDAD
                FROM ALQUILER A
                JOIN VEHICULO V ON A.ID_VEHICULO = V.ID_VEHICULO
                JOIN DETALLE_VEHICULO D ON V.ID_DETALLE_VEHICULO = D.ID_DETALLE_VEHICULO
                GROUP BY V.ID_VEHICULO, V.PATENTE, D.MODELO
                ORDER BY CANTIDAD DESC
                LIMIT 5
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()


    def obtener_facturacion_mensual(self, anio):
        """Suma de COSTO_TOTAL agrupado por mes para un año específico."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        try:
            # DATE_FORMAT('%Y-%m') agrupa por "2023-11", "2023-12", etc.
            sql = """
                SELECT 
                    DATE_FORMAT(FEC_FIN, '%%M') as MES_NOMBRE, 
                    MONTH(FEC_FIN) as MES_NUMERO,
                    SUM(COSTO_TOTAL) as TOTAL
                FROM ALQUILER
                WHERE YEAR(FEC_FIN) = %s AND ID_ESTADO = 7
                GROUP BY MES_NUMERO, MES_NOMBRE
                ORDER BY MES_NUMERO ASC
            """
            cursor.execute(sql, (anio,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()


    def alquileres_por_periodo(self, fecha_desde, fecha_hasta):
        """Cantidad de alquileres iniciados en un rango de fechas."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
                SELECT A.*, C.NOMBRE as CLIENTE, D.MODELO, V.PATENTE
                FROM ALQUILER A
                JOIN CLIENTE C ON A.ID_CLIENTE = C.ID_CLIENTE
                JOIN VEHICULO V ON A.ID_VEHICULO = V.ID_VEHICULO
                JOIN DETALLE_VEHICULO D ON V.ID_DETALLE_VEHICULO = D.ID_DETALLE_VEHICULO
                WHERE A.FEC_INICIO BETWEEN %s AND %s
            """
            cursor.execute(sql, (fecha_desde, fecha_hasta))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
            
            
    def historial_cliente_detallado(self, id_cliente):
        """Listado detallado para un cliente específico."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
                SELECT 
                    A.ID_ALQUILER, 
                    D.MODELO, 
                    V.PATENTE, 
                    A.FEC_INICIO, 
                    A.FEC_FIN, 
                    A.COSTO_TOTAL,
                    E.TX_ESTADO as ESTADO
                FROM ALQUILER A
                JOIN VEHICULO V ON A.ID_VEHICULO = V.ID_VEHICULO
                JOIN DETALLE_VEHICULO D ON V.ID_DETALLE_VEHICULO = D.ID_DETALLE_VEHICULO
                JOIN ESTADO E ON A.ID_ESTADO = E.ID_ESTADO
                WHERE A.ID_CLIENTE = %s
                ORDER BY A.FEC_INICIO DESC
            """
            cursor.execute(sql, (id_cliente,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()