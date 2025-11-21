import sqlite3
from BACK.modelos import TipoMantenimiento
from db_conection import DBConnection


class TipoMantenimientoManager:
    """Clase Manager para manejar la persistencia de objetos TipoMantenimiento."""
    
    def __init__(self):
        self.db_connection = DBConnection()

    def __row_to_tipo_mantenimiento(self, row):
        """Mapea un registro (fila de la BD) a un objeto TipoMantenimiento."""
        if row is None:
            return None
            
        return TipoMantenimiento(
            id_tipo_mantenimiento=row['ID_TIPO_MANTENIMIENTO'],
            tipo_mantenimiento=row['TX_TIPO_MANTENIMIENTO'] # Usamos TX_TIPO_MANTENIMIENTO
        )

    # --- Método LEER (Consulta por ID) ---
    def obtener_por_id(self, id_tipo_mantenimiento):
        """Busca un tipo de mantenimiento por su ID."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM TIPO_MANTENIMIENTO WHERE ID_TIPO_MANTENIMIENTO = ?", (id_tipo_mantenimiento,))
            row = cursor.fetchone()
            return self.__row_to_tipo_mantenimiento(row)
        finally:
            conn.close()

    # --- Método LEER TODO (Listado) ---
    def listar_todos(self):
        """Retorna una lista de todos los objetos TipoMantenimiento."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM TIPO_MANTENIMIENTO")
            tipos = [self.__row_to_tipo_mantenimiento(row) for row in cursor.fetchall()]
            return tipos
        finally:
            conn.close()
            