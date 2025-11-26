# EmpleadoManager.py

import sqlite3
from BACK.modelos import Empleado
from ..db_conection import DBConnection

class EmpleadoManager:
    """Clase Manager para manejar la persistencia de objetos Empleado (ABM)."""
    
    def __init__(self):
        self.db_connection = DBConnection()

    def __row_to_empleado(self, row):
        """Mapea un registro (fila de la BD) a un objeto Empleado."""
        if row is None:
            return None
            
        return Empleado(
            id_empleado=row['ID_EMPLEADO'],
            nombre=row['NOMBRE'],
            dni=row['DNI'],
            mail=row['MAIL']
        )
        
    # --- 1. Método CREAR (Alta) ---
    def guardar(self, empleado):
        """Inserta un nuevo empleado en la BD y asigna su ID."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO EMPLEADO (NOMBRE, DNI, MAIL) 
                VALUES (?, ?, ?)
            """, (empleado.nombre, empleado.dni, empleado.mail))
            
            empleado.id_empleado = cursor.lastrowid
            conn.commit()
            return empleado
        except sqlite3.Error as e:
            print(f"Error al guardar el empleado: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    # --- 2. Método LEER (Consulta por ID) ---
    def obtener_por_id(self, id_empleado):
        """Busca un empleado por su ID y retorna un objeto Empleado."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM EMPLEADO WHERE ID_EMPLEADO = ?", (id_empleado,))
            row = cursor.fetchone()
            
            return self.__row_to_empleado(row)
            
        except sqlite3.Error as e:
            print(f"Error al obtener empleado: {e}")
            return None
        finally:
            conn.close()
        

    # -- 3. Método LEER TODO (Listado) ---
    def listar_todos(self):
        """Retorna una lista de todos los objetos Empleado."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM EMPLEADO")
            
            empleados = [self.__row_to_empleado(row) for row in cursor.fetchall()]
            return empleados
        except sqlite3.Error as e:
            print(f"Error al listar empleados: {e}")
            return []
        finally:
            conn.close()


    # --- 4. Método ACTUALIZAR --- (Modificación) ---
    def actualizar(self, empleado):
        """Actualiza los datos de un empleado existente en la BD."""
        if not empleado.id_empleado:
            print("Error: No se puede actualizar un empleado sin ID.")
            return False
            
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE EMPLEADO 
                SET NOMBRE = ?, DNI = ?, MAIL = ? 
                WHERE ID_EMPLEADO = ?
            """, (empleado.nombre, empleado.dni, empleado.mail, empleado.id_empleado))
            
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar el empleado: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()


    # --- 5. Método ELIMINAR ---
    def eliminar(self, id_empleado):
        """Elimina un empleado de la base de datos por su ID."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM EMPLEADO WHERE ID_EMPLEADO = ?", (id_empleado,))
            conn.commit()
            return cursor.rowcount > 0  # Retorna True si se eliminó algún registro
        except sqlite3.Error as e:
            print(f"Error al eliminar el empleado: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()