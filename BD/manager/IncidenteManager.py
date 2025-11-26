# IncidenteManager.py

import sqlite3
from datetime import datetime
from BACK.modelos import Incidente
from db_conection import DBConnection
# Importamos los Managers de las dependencias
from TipoIncidenteManager import TipoIncidenteManager
# from .AlquilerManager import AlquilerManager # Necesario para resolver la dependencia 'alquiler'

class IncidenteManager:
    """Clase Manager para manejar la persistencia de objetos Incidente."""
    
    def __init__(self):
        self.db_connection = DBConnection()
        self.tipo_incidente_manager = TipoIncidenteManager()
        # self.alquiler_manager = AlquilerManager() # Descomentar cuando exista


    def __row_to_incidente(self, row):
        """Mapea un registro a un objeto Incidente, resolviendo dependencias."""
        if row is None:
            return None
            
        # 1. Resolver dependencias
        tipo_incidente_obj = self.tipo_incidente_manager.obtener_por_id(row['ID_TIPO_INCIDENTE'])
        
        # Temporal: Alquiler lo dejamos como None hasta implementar AlquilerManager
        # alquiler_obj = self.alquiler_manager.obtener_por_id(row['ID_ALQUILER']) 
        alquiler_obj = row['ID_ALQUILER'] 

        fec_incidente = datetime.strptime(row['FEC_INCIDENTE'], '%Y-%m-%d %H:%M:%S') if row['FEC_INCIDENTE'] else None
        
        # 2. Crear y retornar el objeto Incidente
        return Incidente(
            id_incidente=row['ID_INCIDENTE'],
            tipo_incidente=tipo_incidente_obj,
            alquiler=alquiler_obj, # Usamos el ID temporalmente
            fecha_incidente=fec_incidente,
            descripcion=row['DESCRIPCION'],
            costo=row['COSTO']
        )


    # --- 1. Método CREAR (Alta) ---
    def guardar(self, incidente):
        """Inserta un nuevo registro de incidente en la BD."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            fec_incidente_str = incidente.fecha_incidente.strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute("""
                INSERT INTO INCIDENTE (ID_TIPO_INCIDENTE, ID_ALQUILER, FEC_INCIDENTE, DESCRIPCION, COSTO) 
                VALUES (?, ?, ?, ?, ?)
                """, (incidente.tipo_incidente.id_tipo_incidente, 
                    incidente.alquiler.id_alquiler, # Asumimos que el objeto Alquiler tiene ID
                    fec_incidente_str, 
                    incidente.descripcion, 
                    incidente.costo))
            
            incidente.id_incidente = cursor.lastrowid
            conn.commit()
            return incidente
        except sqlite3.Error as e:
            print(f"Error al guardar el incidente: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()


    # --- 2. Método LEER (Consulta por ID) ---
    def obtener_por_id(self, id_incidente):
        """Busca un incidente por su ID."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM INCIDENTE WHERE ID_INCIDENTE = ?", (id_incidente,))
            row = cursor.fetchone()
            return self.__row_to_incidente(row)
        finally:
            conn.close()


    # -- 3. Método LEER TODO (Listado) ---
    def listar_todos(self):
        """Retorna una lista de todos los objetos Incidente."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM INCIDENTE")
            rows = cursor.fetchall()
            incidentes = [self.__row_to_incidente(row) for row in rows]
            return incidentes
        finally:
            conn.close()


    # --- 4. Método ACTUALIZAR --- (Modificación) ---
    def actualizar(self, incidente):
        """Actualiza un incidente existente en la BD."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            fec_incidente_str = incidente.fecha_incidente.strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute("""
                UPDATE INCIDENTE 
                SET ID_TIPO_INCIDENTE = ?, ID_ALQUILER = ?, FEC_INCIDENTE = ?, DESCRIPCION = ?, COSTO = ?
                WHERE ID_INCIDENTE = ?
                """, (incidente.tipo_incidente.id_tipo_incidente, 
                    incidente.alquiler.id_alquiler, 
                    fec_incidente_str, 
                    incidente.descripcion, 
                    incidente.costo,
                    incidente.id_incidente))
            
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar el incidente: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()