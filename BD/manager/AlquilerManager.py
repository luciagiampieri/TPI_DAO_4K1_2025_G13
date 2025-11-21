import sqlite3
from datetime import datetime
from BACK.modelos import Alquiler
from db_conection import DBConnection
from VehiculoManager import VehiculoManager 
from ClienteManager import ClienteManager 
from EmpleadoManager import EmpleadoManager 
from EstadoManager import EstadoManager 

class AlquilerManager:
    """Clase Manager para manejar SOLO la persistencia (CRUD) de objetos Alquiler."""
    
    def __init__(self):
        self.db_connection = DBConnection()
        self.vehiculo_manager = VehiculoManager()
        self.cliente_manager = ClienteManager()
        self.empleado_manager = EmpleadoManager()
        self.estado_manager = EstadoManager()

    def __row_to_alquiler(self, row):
        """Mapea un registro a un objeto Alquiler, resolviendo dependencias."""
        if row is None:
            return None
            
        # 1. Resolver dependencias
        vehiculo_obj = self.vehiculo_manager.obtener_por_id(row['ID_VEHICULO'])
        cliente_obj = self.cliente_manager.obtener_por_id(row['ID_CLIENTE'])
        empleado_obj = self.empleado_manager.obtener_por_id(row['ID_EMPLEADO'])
        estado_obj = self.estado_manager.obtener_por_id(row['ID_ESTADO'])
        
        # Las fechas deben convertirse de string a objeto datetime
        fec_inicio = datetime.strptime(row['FEC_INICIO'], '%Y-%m-%d %H:%M:%S')
        fec_fin = datetime.strptime(row['FEC_FIN'], '%Y-%m-%d %H:%M:%S')
        
        # 2. Crear y retornar el objeto Alquiler
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

    
    # --- 1. Método CREAR (Alta de Alquiler) ---
    def guardar(self, alquiler):
        """Inserta un nuevo alquiler en la BD."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            fec_inicio_str = alquiler.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')
            fec_fin_str = alquiler.fecha_fin.strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute("""
                INSERT INTO ALQUILER (ID_VEHICULO, ID_EMPLEADO, ID_CLIENTE, FEC_INICIO, FEC_FIN, COSTO_TOTAL, ID_ESTADO) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (alquiler.vehiculo.id_vehiculo, 
                  alquiler.empleado.id_empleado, 
                  alquiler.cliente.id_cliente, 
                  fec_inicio_str, 
                  fec_fin_str, 
                  alquiler.costo_total, 
                  alquiler.estado.id_estado)
            )
            
            alquiler.id_alquiler = cursor.lastrowid
            conn.commit()
            print(f"✅ Alquiler ID {alquiler.id_alquiler} persistido.")
            return alquiler
        except sqlite3.Error as e:
            print(f"Error al guardar el alquiler: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    # --- 2. Método LEER (Consulta por ID) ---
    def obtener_por_id(self, id_alquiler):
        """Busca un alquiler por su ID y retorna un objeto Alquiler."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM ALQUILER WHERE ID_ALQUILER = ?", (id_alquiler,))
            row = cursor.fetchone()
            
            return self.__row_to_alquiler(row)
            
        except sqlite3.Error as e:
            print(f"Error al obtener alquiler: {e}")
            return None
        finally:
            conn.close()
            
    # --- 3. Método LEER TODO (Listado) ---
    def listar_todos(self):
        """Retorna una lista de todos los objetos Alquiler."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM ALQUILER")
            alquileres = [self.__row_to_alquiler(row) for row in cursor.fetchall()]
            return alquileres
        except sqlite3.Error as e:
            print(f"Error al listar alquileres: {e}")
            return []
        finally:
            conn.close()

    # --- 4. Método ACTUALIZAR (Modificación) ---
    def actualizar(self, alquiler):
        """Actualiza los datos de un alquiler existente en la BD."""
        if not alquiler.id_alquiler:
            print("Error: No se puede actualizar un alquiler sin ID.")
            return False
            
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            fec_inicio_str = alquiler.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')
            fec_fin_str = alquiler.fecha_fin.strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute("""
                UPDATE ALQUILER SET 
                    ID_VEHICULO = ?, ID_EMPLEADO = ?, ID_CLIENTE = ?, 
                    FEC_INICIO = ?, FEC_FIN = ?, COSTO_TOTAL = ?, ID_ESTADO = ?
                WHERE ID_ALQUILER = ?
            """, (alquiler.vehiculo.id_vehiculo, alquiler.empleado.id_empleado, alquiler.cliente.id_cliente, 
                  fec_inicio_str, fec_fin_str, alquiler.costo_total, alquiler.estado.id_estado, 
                  alquiler.id_alquiler))
            
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar el alquiler: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    # --- 5. Método BORRAR (Baja) ---
    def eliminar(self, id_alquiler):
        """Elimina un alquiler por su ID."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM ALQUILER WHERE ID_ALQUILER = ?", (id_alquiler,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar alquiler: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()