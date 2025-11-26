import sqlite3
from datetime import datetime
from BACK.modelos import Mantenimiento
from ..db_conection import DBConnection
from .VehiculoManager import VehiculoManager 
from .TipoMantenimientoManager import TipoMantenimientoManager 

class MantenimientoManager:
    """Clase Manager para manejar la persistencia de objetos Mantenimiento."""
    
    def __init__(self):
        self.db_connection = DBConnection()
        self.vehiculo_manager = VehiculoManager()
        self.tipo_mantenimiento_manager = TipoMantenimientoManager()


    def __row_to_mantenimiento(self, row):
        """Mapea un registro a un objeto Mantenimiento, resolviendo dependencias."""
        if row is None:
            return None
            
        # 1. Resolver dependencias
        vehiculo_obj = self.vehiculo_manager.obtener_por_id(row['ID_VEHICULO'])
        tipo_mantenimiento_obj = self.tipo_mantenimiento_manager.obtener_por_id(row['ID_TIPO_MANTENIMIENTO'])
        
        # Las fechas deben convertirse de string a objeto datetime
        fec_inicio = datetime.strptime(row['FEC_INICIO'], '%Y-%m-%d %H:%M:%S') if row['FEC_INICIO'] else None
        fec_fin = datetime.strptime(row['FEC_FIN'], '%Y-%m-%d %H:%M:%S') if row['FEC_FIN'] else None
        
        # 2. Crear y retornar el objeto Mantenimiento
        return Mantenimiento(
            id_mantenimiento=row['ID_MANTENIMIENTO'],
            vehiculo=vehiculo_obj,
            tipo_mantenimiento=tipo_mantenimiento_obj,
            fecha_inicio=fec_inicio,
            fecha_fin=fec_fin,
            costo=row['COSTO'],
            observacion=row['OBSERVACION']
        )


    # --- 1. Método CREAR (Alta) ---
    def guardar(self, mantenimiento):
        """Inserta un nuevo registro de mantenimiento en la BD."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            # Los objetos datetime deben formatearse como string para SQLite
            fec_inicio_str = mantenimiento.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')
            fec_fin_str = mantenimiento.fecha_fin.strftime('%Y-%m-%d %H:%M:%S') if mantenimiento.fecha_fin else None

            cursor.execute("""
                INSERT INTO MANTENIMIENTO (ID_VEHICULO, ID_TIPO_MANTENIMIENTO, FEC_INICIO, FEC_FIN, COSTO, OBSERVACION) 
                VALUES (?, ?, ?, ?, ?, ?)
                """, (mantenimiento.vehiculo.id_vehiculo, 
                    mantenimiento.tipo_mantenimiento.id_tipo_mantenimiento, 
                    fec_inicio_str, 
                    fec_fin_str, 
                    mantenimiento.costo, 
                    mantenimiento.observacion))
            
            mantenimiento.id_mantenimiento = cursor.lastrowid
            conn.commit()
            return mantenimiento
        except sqlite3.Error as e:
            print(f"Error al guardar el mantenimiento: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()


    # --- 2. Método LEER (Consulta por ID) ---
    def obtener_por_id(self, id_mantenimiento):
        """Busca un mantenimiento por su ID."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM MANTENIMIENTO WHERE ID_MANTENIMIENTO = ?", (id_mantenimiento,))
            row = cursor.fetchone()
            return self.__row_to_mantenimiento(row)
        finally:
            conn.close()


    # Además, se necesitaría un método para finalizar un mantenimiento (UPDATE de FEC_FIN y COSTO)
    def finalizar_mantenimiento(self, id_mantenimiento, fecha_fin, costo):
        """Actualiza el registro de mantenimiento con fecha de fin y costo."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        try:
            fec_fin_str = fecha_fin.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                UPDATE MANTENIMIENTO SET FEC_FIN = ?, COSTO = ? WHERE ID_MANTENIMIENTO = ?
            """, (fec_fin_str, costo, id_mantenimiento))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()