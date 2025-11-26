import pymysql
from datetime import datetime

from BACK.modelos.Alquiler import Alquiler
from ..db_conection import DBConnection

from .VehiculoManager import VehiculoManager 
from .ClienteManager import ClienteManager 
from .EmpleadoManager import EmpleadoManager 
from .EstadoManager import EstadoManager


class AlquilerManager:
    """Manager para manejar la persistencia de objetos Alquiler (MySQL)."""

    def __init__(self):
        self.db_connection = DBConnection()
        self.vehiculo_manager = VehiculoManager()
        self.cliente_manager = ClienteManager()
        self.empleado_manager = EmpleadoManager()
        self.estado_manager = EstadoManager()

    # ----------------------------------------------------------
    #   MAPEO FILA → OBJETO ALQUILER
    # ----------------------------------------------------------
    def __row_to_alquiler(self, row):
        if row is None:
            return None

        # Resolver dependencias
        vehiculo_obj = self.vehiculo_manager.obtener_por_id(row['ID_VEHICULO'])
        cliente_obj = self.cliente_manager.obtener_por_id(row['ID_CLIENTE'])
        empleado_obj = self.empleado_manager.obtener_por_id(row['ID_EMPLEADO'])
        estado_obj = self.estado_manager.obtener_por_id(row['ID_ESTADO'])

        # Convertir fechas desde string MySQL
        fec_inicio = datetime.strptime(row['FEC_INICIO'], '%Y-%m-%d %H:%M:%S')
        fec_fin = datetime.strptime(row['FEC_FIN'], '%Y-%m-%d %H:%M:%S')

        return Alquiler(
            id_alquiler=row['ID_ALQUILER'],
            vehiculo=vehiculo_obj,
            cliente=cliente_obj,
            empleado=empleado_obj,
            fecha_inicio=fec_inicio,
            fecha_fin=fec_fin,
            costo_total=row['COSTO_TOTAL'],
            estado=estado_obj
        )

    # ----------------------------------------------------------
    #   CREAR
    # ----------------------------------------------------------
    def guardar(self, alquiler):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            fec_inicio_str = alquiler.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')
            fec_fin_str = alquiler.fecha_fin.strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute("""
                INSERT INTO ALQUILER 
                    (ID_VEHICULO, ID_EMPLEADO, ID_CLIENTE, 
                     FEC_INICIO, FEC_FIN, COSTO_TOTAL, ID_ESTADO)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                alquiler.vehiculo.id_vehiculo,
                alquiler.empleado.id_empleado,
                alquiler.cliente.id_cliente,
                fec_inicio_str,
                fec_fin_str,
                alquiler.costo_total,
                alquiler.estado.id_estado
            ))

            alquiler.id_alquiler = cursor.lastrowid
            conn.commit()
            return alquiler

        except pymysql.MySQLError as e:
            print(f"Error al guardar alquiler: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   OBTENER POR ID
    # ----------------------------------------------------------
    def obtener_por_id(self, id_alquiler):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM ALQUILER WHERE ID_ALQUILER = %s", (id_alquiler,))
            row = cursor.fetchone()
            return self.__row_to_alquiler(row)

        except pymysql.MySQLError as e:
            print(f"Error al obtener alquiler: {e}")
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
            cursor.execute("SELECT * FROM ALQUILER")
            rows = cursor.fetchall()
            return [self.__row_to_alquiler(row) for row in rows]

        except pymysql.MySQLError as e:
            print(f"Error al listar alquileres: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   ACTUALIZAR
    # ----------------------------------------------------------
    def actualizar(self, alquiler):
        if not alquiler.id_alquiler:
            print("Error: alquiler sin ID.")
            return False

        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            fec_inicio_str = alquiler.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')
            fec_fin_str = alquiler.fecha_fin.strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute("""
                UPDATE ALQUILER SET 
                    ID_VEHICULO = %s,
                    ID_EMPLEADO = %s,
                    ID_CLIENTE = %s,
                    FEC_INICIO = %s,
                    FEC_FIN = %s,
                    COSTO_TOTAL = %s,
                    ID_ESTADO = %s
                WHERE ID_ALQUILER = %s
            """, (
                alquiler.vehiculo.id_vehiculo,
                alquiler.empleado.id_empleado,
                alquiler.cliente.id_cliente,
                fec_inicio_str,
                fec_fin_str,
                alquiler.costo_total,
                alquiler.estado.id_estado,
                alquiler.id_alquiler
            ))

            conn.commit()
            return cursor.rowcount > 0

        except pymysql.MySQLError as e:
            print(f"Error al actualizar alquiler: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   CANCELAR (CAMBIAR ESTADO)
    # ----------------------------------------------------------
    def cancelar(self, alquiler):
        if not alquiler.id_alquiler:
            print("Error: alquiler sin ID.")
            return False

        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            fec_inicio_str = alquiler.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')
            fec_fin_str = alquiler.fecha_fin.strftime('%Y-%m-%d %H:%M:%S')

            CANCELADO_ID = 5  # Ajustá según tu tabla ESTADO

            cursor.execute("""
                UPDATE ALQUILER SET 
                    ID_ESTADO = %s,
                    FEC_INICIO = %s,
                    FEC_FIN = %s
                WHERE ID_ALQUILER = %s
            """, (
                CANCELADO_ID,
                fec_inicio_str,
                fec_fin_str,
                alquiler.id_alquiler
            ))

            conn.commit()
            return cursor.rowcount > 0

        except pymysql.MySQLError as e:
            print(f"Error al cancelar alquiler: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   LISTAR POR CLIENTE
    # ----------------------------------------------------------
    def listar_por_cliente(self, id_cliente):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM ALQUILER WHERE ID_CLIENTE = %s", (id_cliente,))
            rows = cursor.fetchall()
            return [self.__row_to_alquiler(row) for row in rows]

        except pymysql.MySQLError as e:
            print(f"Error al listar alquileres por cliente: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
