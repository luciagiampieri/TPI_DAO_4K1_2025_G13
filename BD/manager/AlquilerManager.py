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
        fec_inicio = row['FEC_INICIO']
        fec_fin = row['FEC_FIN']

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

    def finalizar_con_kilometraje(self, alquiler):
        """
        Actualiza el alquiler (fin, costo, estado) y el kilometraje/estado del vehículo
        en una sola transacción atómica.
        """
        if not alquiler.id_alquiler or not alquiler.vehiculo.id_vehiculo:
            return False

        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            # Datos para el Alquiler
            fec_fin_str = alquiler.fecha_fin.strftime('%Y-%m-%d %H:%M:%S')
            
            # 1. Actualizar ALQUILER
            cursor.execute("""
                UPDATE ALQUILER SET 
                    FEC_FIN = %s,
                    COSTO_TOTAL = %s,
                    ID_ESTADO = %s
                WHERE ID_ALQUILER = %s
            """, (
                fec_fin_str,
                alquiler.costo_total,
                alquiler.estado.id_estado,
                alquiler.id_alquiler
            ))

            ESTADO_DISPONIBLE = 1
            
            cursor.execute("""
                UPDATE VEHICULO SET
                    KILOMETRAJE = %s,
                    ID_ESTADO = %s
                WHERE ID_VEHICULO = %s
            """, (
                alquiler.vehiculo.kilometraje,
                ESTADO_DISPONIBLE,
                alquiler.vehiculo.id_vehiculo
            ))

            conn.commit()
            return True

        except pymysql.MySQLError as e:
            print(f"Error al finalizar alquiler y actualizar vehículo: {e}")
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

    def listar_activo_por_vehiculo(self, id_vehiculo):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM ALQUILER WHERE ID_VEHICULO = %s AND (ID_ESTADO = 7 OR ID_ESTADO = 6)", (id_vehiculo,))
            rows = cursor.fetchall()
            return [self.__row_to_alquiler(row) for row in rows]

        except pymysql.MySQLError as e:
            print(f"Error al listar alquileres por vehículo: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def verificar_disponibilidad_sp(self, id_vehiculo, fecha_inicio, fecha_fin):
        """
        Llama al SP. 
        - Si no pasa nada: Retorna True (Disponible).
        - Si el SP lanza SIGNAL 45000: Retorna False (No disponible).
        """
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            # 1. Llamar al SP con los 3 parámetros
            cursor.callproc('SP_VALIDAR_DISPONIBILIDAD_ALQUILER', (
                id_vehiculo, 
                fecha_inicio, 
                fecha_fin
            ))
            
            return True

        except pymysql.err.OperationalError as e:
            # El código 1644 es el genérico para "User defined signal" en MySQL
            code, message = e.args
            
            if code == 1644 and 'CONFLICTO_FECHAS' in message:
                print(f"⚠️ Validación falló: {message}")
                return False
            
            # Si es otro error (conexión, sintaxis, etc), lo dejamos subir o lo imprimimos
            print(f"❌ Error inesperado de BD: {e}")
            return False
            
        except Exception as e:
            print(f"❌ Error general: {e}")
            return False
            
        finally:
            cursor.close()
            conn.close()



