import sqlite3
from BACK.modelos import CaracteristicaVehiculo, Categoria 
from .CategoriaManager import CategoriaManager
from ..db_conection import DBConnection
from .CategoriaManager import CategoriaManager


class CaracteristicaVehiculoManager:
    def __init__(self):
        self.db_connection = DBConnection()
        self.categoria_manager = CategoriaManager() # Inyección de dependencia para obtener el objeto Categoria


    def __row_to_caracteristica(self, row):
        """Mapea un registro a un objeto CaracteristicaVehiculo, resolviendo la dependencia Categoria."""
        if row is None:
            return None
            
        # 1. Obtener el objeto Categoria completo usando su ID
        categoria_obj = self.categoria_manager.obtener_por_id(row['ID_CATEGORIA'])
        
        # 2. Crear y retornar el objeto CaracteristicaVehiculo
        return CaracteristicaVehiculo(
            id_caracteristica=row['ID_DETALLE_VEHICULO'], # Usamos el nombre de la tabla de tu SQL
            modelo=row['MODELO'],
            anio=row['AÑO'],
            categoria=categoria_obj # Se almacena el objeto Categoria, no el ID
        )


    def guardar(self, caracteristica):
        """Inserta una nueva característica en la BD."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            # Insertamos el ID de la Categoría, no el objeto Categoria
            categoria_id = caracteristica.categoria.id_categoria
            
            cursor.execute("""
                INSERT INTO DETALLE_VEHICULO (MODELO, "AÑO", ID_CATEGORIA) 
                VALUES (?, ?, ?)
            """, (caracteristica.modelo, caracteristica.anio, categoria_id))
            
            caracteristica.id_caracteristica = cursor.lastrowid
            conn.commit()
            return caracteristica
        except sqlite3.Error as e:
            print(f"Error al guardar CaracteristicaVehiculo: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
            
    
    def obtener_por_id(self, id_caracteristica):
        """Busca una característica por su ID."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM DETALLE_VEHICULO WHERE ID_DETALLE_VEHICULO = ?", (id_caracteristica,))
            row = cursor.fetchone()
            return self.__row_to_caracteristica(row)
        finally:
            conn.close()


    def listar_todos(self):
        """Retorna una lista de todas las características de vehículos."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM DETALLE_VEHICULO")
            rows = cursor.fetchall()
            return [self.__row_to_caracteristica(row) for row in rows]
        finally:
            conn.close()