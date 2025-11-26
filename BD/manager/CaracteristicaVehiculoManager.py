import mysql.connector
from BACK.modelos.CaracteristicaVehiculo import CaracteristicaVehiculo
from ..db_conection import DBConnection
from .CategoriaManager import CategoriaManager


class CaracteristicaVehiculoManager:

    def __init__(self):
        self.db_connection = DBConnection()
        self.categoria_manager = CategoriaManager()

    # ----------------------------------------------------------
    # MAPEAR FILA A OBJETO
    # ----------------------------------------------------------
    def __row_to_caracteristica(self, row):
        if row is None:
            return None

        categoria_obj = self.categoria_manager.obtener_por_id(row['ID_CATEGORIA'])

        return CaracteristicaVehiculo(
            id_caracteristica=row['ID_DETALLE_VEHICULO'],
            modelo=row['MODELO'],
            anio=row['AÑO'],          # Ajustar si usás AÑO en la BD
            categoria=categoria_obj
        )

    # ----------------------------------------------------------
    # INSERTAR REGISTRO
    # ----------------------------------------------------------
    def guardar(self, caracteristica):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO DETALLE_VEHICULO (MODELO, AÑO, ID_CATEGORIA)
                VALUES (%s, %s, %s)
            """, (
                caracteristica.modelo,
                caracteristica.anio,
                caracteristica.categoria.id_categoria
            ))

            caracteristica.id_caracteristica = cursor.lastrowid
            conn.commit()
            return caracteristica

        except mysql.connector.Error as e:
            print(f"Error al guardar CaracteristicaVehiculo: {e}")
            conn.rollback()
            return None

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    # OBTENER POR ID
    # ----------------------------------------------------------
    def obtener_por_id(self, id_caracteristica):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT * 
                FROM DETALLE_VEHICULO 
                WHERE ID_DETALLE_VEHICULO = %s
            """, (id_caracteristica,))

            row = cursor.fetchone()
            return self.__row_to_caracteristica(row)

        finally:
            cursor.close()
            conn.close()

    # ----------------------------------------------------------
    # LISTAR TODOS
    # ----------------------------------------------------------
    def listar_todos(self):
        conn = self.db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM DETALLE_VEHICULO")
            rows = cursor.fetchall()
            return [self.__row_to_caracteristica(row) for row in rows]

        finally:
            cursor.close()
            conn.close()

    def crear_detalle(self, modelo, anio, categoria):
        nueva_caracteristica = CaracteristicaVehiculo(
            id_caracteristica=None,
            modelo=modelo,
            anio=anio,
            categoria=categoria
        )
        return self.guardar(nueva_caracteristica)
