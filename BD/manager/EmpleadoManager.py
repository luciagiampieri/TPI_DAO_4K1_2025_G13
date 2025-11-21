# EmpleadoManager.py

import sqlite3
from BACK.modelos import Empleado
from db_conection import DBConnection

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
            
    # También necesitarías los métodos listar_todos, actualizar y eliminar.