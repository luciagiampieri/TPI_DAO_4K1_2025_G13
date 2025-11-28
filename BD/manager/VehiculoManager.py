import pymysql
from BACK.modelos.Vehiculo import Vehiculo
from ..db_conection import DBConnection
from .EstadoManager import EstadoManager
from .CaracteristicaVehiculoManager import CaracteristicaVehiculoManager


class VehiculoManager:
    """Manager para manejar la persistencia de objetos Vehiculo (ABM)."""

    def __init__(self):
        self.db_connection = DBConnection()
        self.estado_manager = EstadoManager()
        self.caracteristica_manager = CaracteristicaVehiculoManager()

    # ----------------------------------------------------------
    #   MAPEO FILA → OBJETO
    # ----------------------------------------------------------
    def __row_to_vehiculo(self, row):
        if row is None:
            return None
        
        print("Row en VehiculoManager:", row)

        estado_obj = self.estado_manager.obtener_por_id(row["ID_ESTADO"])

        print("Estado obtenido:", estado_obj)
        caracteristica_obj = self.caracteristica_manager.obtener_por_id(row["ID_DETALLE_VEHICULO"])

        return Vehiculo(
            id_vehiculo=row["ID_VEHICULO"],
            caracteristica_vehiculo=caracteristica_obj,
            estado=estado_obj,
            patente=row["PATENTE"],
            kilometraje=row["KILOMETRAJE"],
            costo_diario=row["COSTO_DIARIO_ALQUILER"]
        )

    # ----------------------------------------------------------
    #   CREAR
    # ----------------------------------------------------------
    def guardar(self, vehiculo):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO VEHICULO 
                (ID_DETALLE_VEHICULO, ID_ESTADO, PATENTE, KILOMETRAJE, COSTO_DIARIO_ALQUILER)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                vehiculo.caracteristica_vehiculo.id_caracteristica,
                vehiculo.estado.id_estado,
                vehiculo.patente,
                vehiculo.kilometraje,
                vehiculo.costo_diario
            ))

            vehiculo.id_vehiculo = cursor.lastrowid
            conn.commit()
            return vehiculo

        except pymysql.MySQLError as e:
            print(f"Error al guardar el vehículo: {e}")
            conn.rollback()
            return None

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   OBTENER POR ID
    # ----------------------------------------------------------
    def obtener_por_id(self, id_vehiculo):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * 
                FROM VEHICULO 
                WHERE ID_VEHICULO = %s
            """, (id_vehiculo,))

            row = cursor.fetchone()
            return self.__row_to_vehiculo(row)

        except pymysql.MySQLError as e:
            print(f"Error al obtener vehículo: {e}")
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
            cursor.execute("SELECT * FROM VEHICULO")
            rows = cursor.fetchall()
            return [self.__row_to_vehiculo(row) for row in rows]

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   ACTUALIZAR
    # ----------------------------------------------------------
    def actualizar(self, vehiculo):
        if not vehiculo.id_vehiculo:
            print("Error: No se puede actualizar un vehículo sin ID.")
            return False

        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE VEHICULO
                SET ID_DETALLE_VEHICULO = %s,
                    ID_ESTADO = %s,
                    PATENTE = %s,
                    KILOMETRAJE = %s,
                    COSTO_DIARIO_ALQUILER = %s
                WHERE ID_VEHICULO = %s
            """, (
                vehiculo.caracteristica_vehiculo.id_caracteristica,
                vehiculo.estado.id_estado,
                vehiculo.patente,
                vehiculo.kilometraje,
                vehiculo.costo_diario,
                vehiculo.id_vehiculo
            ))

            conn.commit()
            return True

        except pymysql.MySQLError as e:
            print(f"Error al actualizar vehículo: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   ELIMINAR
    # ----------------------------------------------------------
    def eliminar(self, id_vehiculo):
        conn = self.db_connection.get_connection()
        if conn is None: return False
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT ID_DETALLE_VEHICULO FROM VEHICULO WHERE ID_VEHICULO = %s", (id_vehiculo,))
            row = cursor.fetchone()
            
            if not row:
                print(f"Error: Vehículo con ID {id_vehiculo} no encontrado.")
                return False
                
            id_detalle = row['ID_DETALLE_VEHICULO'] 
            
            cursor.execute("DELETE FROM VEHICULO WHERE ID_VEHICULO = %s", (id_vehiculo,))

            cursor.execute("""
                DELETE FROM DETALLE_VEHICULO
                WHERE ID_DETALLE_VEHICULO = %s
                AND NOT EXISTS (
                    SELECT 1 FROM VEHICULO WHERE ID_DETALLE_VEHICULO = %s
                )
            """, (id_detalle, id_detalle))
            
            conn.commit()
            return True

        except pymysql.MySQLError as e:
            print(f"Error al eliminar vehículo: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    #   ACTUALIZAR ESTADO (SOLO LA COLUMNA ID_ESTADO)
    # ----------------------------------------------------------
    def actualizar_estado(self, id_vehiculo, nuevo_estado_id):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE VEHICULO 
                SET ID_ESTADO = %s
                WHERE ID_VEHICULO = %s
            """, (nuevo_estado_id, id_vehiculo))

            conn.commit()
            return cursor.rowcount > 0

        except pymysql.MySQLError as e:
            print(f"Error al actualizar estado del vehículo: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    def verificar_mantenimiento_activo(self, id_vehiculo):
        """
        Llama al SP para ver si el vehículo tiene un mantenimiento activo en este momento.
        Retorna True si hay mantenimiento, False si no.
        """
        conn = self.db_connection.get_connection()
        cursor = conn.cursor() # Ya viene configurado como DictCursor

        try:
            cursor.callproc('SP_VALIDAR_ESTADO_MANTENIMIENTO', (id_vehiculo,))
            resultado = cursor.fetchone()
            
            if resultado:
                return True
            else:
                return False

        except Exception as e:
            print(f"Error al ejecutar SP de validación: {e}")
            return False # En caso de error, asumimos False o manejas la excepción
            
        finally:
            cursor.close()
            conn.close()
