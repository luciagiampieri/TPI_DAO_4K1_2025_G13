import sqlite3
from BACK.modelos import Vehiculo 
from db_conection import DBConnection
from EstadoManager import EstadoManager
from CaracteristicasManager import CaracteristicaVehiculoManager 


class VehiculoManager:
    """Clase Manager para manejar la persistencia de objetos Vehiculo (ABM)."""
    
    def __init__(self):
        self.db_connection = DBConnection()
        self.estado_manager = EstadoManager()
        self.caracteristica_manager = CaracteristicaVehiculoManager()

    def __row_to_vehiculo(self, row):
        """Mapea un registro (fila de la BD) a un objeto Vehiculo, resolviendo todas las dependencias."""
        if row is None:
            return None
            
        # 1. Resolver dependencias
        estado_obj = self.estado_manager.obtener_por_id(row['ID_ESTADO'])
        caracteristica_obj = self.caracteristica_manager.obtener_por_id(row['ID_DETALLE_VEHICULO'])
        
        # 2. Crear y retornar el objeto Vehiculo
        return Vehiculo(
            id_vehiculo=row['ID_VEHICULO'],
            caracteristica_vehiculo=caracteristica_obj,
            estado=estado_obj,
            patente=row['PATENTE'],
            kilometraje=row['KILOMETRAJE'],
            costo_diario=row['COSTO_DIARIO_ALQUILER']
        )

    # --- 1. Método CREAR (Alta) ---
    def guardar(self, vehiculo):
        """Inserta un nuevo vehículo en la BD y asigna su ID."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            # Obtenemos los IDs de las dependencias (el objeto debe tenerlas previamente)
            estado_id = vehiculo.estado.id_estado 
            caracteristica_id = vehiculo.caracteristica_vehiculo.id_caracteristica

            cursor.execute("""
                INSERT INTO VEHICULO (ID_DETALLE_VEHICULO, ID_ESTADO, PATENTE, KILOMETRAJE, COSTO_DIARIO_ALQUILER) 
                VALUES (?, ?, ?, ?, ?)
            """, (caracteristica_id, estado_id, vehiculo.patente, vehiculo.kilometraje, vehiculo.costo_diario))
            
            vehiculo.id_vehiculo = cursor.lastrowid
            conn.commit()
            return vehiculo
        except sqlite3.Error as e:
            print(f"Error al guardar el vehículo: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    # --- 2. Método LEER (Consulta por ID) ---
    def obtener_por_id(self, id_vehiculo):
        """Busca un vehículo por su ID y retorna un objeto Vehiculo."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM VEHICULO WHERE ID_VEHICULO = ?", (id_vehiculo,))
            row = cursor.fetchone()
            
            return self.__row_to_vehiculo(row)
            
        except sqlite3.Error as e:
            print(f"Error al obtener vehículo: {e}")
            return None
        finally:
            conn.close()
            
    # También necesitarías los métodos listar_todos, actualizar y eliminar.
    
    # --- Lógica de negocio específica del DAO ---
    def actualizar_estado(self, id_vehiculo, nuevo_estado_id):
        """Actualiza solo el estado del vehículo, usado al alquilar/finalizar."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE VEHICULO SET ID_ESTADO = ? WHERE ID_VEHICULO = ?", (nuevo_estado_id, id_vehiculo))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar estado del vehículo: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()