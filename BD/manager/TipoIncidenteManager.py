import sqlite3
from BACK.modelos import TipoIncidente
from db_conection import DBConnection

class TipoIncidenteManager:
    """Clase Manager para manejar la persistencia de objetos TipoIncidente."""
    
    def __init__(self):
        self.db_connection = DBConnection()

    def __row_to_tipo_incidente(self, row):
        """Mapea un registro (fila de la BD) a un objeto TipoIncidente."""
        if row is None:
            return None
            
        return TipoIncidente(
            id_tipo_incidente=row['ID_TIPO_INCIDENTE'],
            tipo_incidente=row['TX_INCIDENTE'] # Usamos TX_INCIDENTE
        )

    # --- Método LEER (Consulta por ID) ---
    def obtener_por_id(self, id_tipo_incidente):
        """Busca un tipo de incidente por su ID."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM TIPO_INCIDENTE WHERE ID_TIPO_INCIDENTE = ?", (id_tipo_incidente,))
            row = cursor.fetchone()
            return self.__row_to_tipo_incidente(row)
        finally:
            conn.close()
            
    def listar_todos(self):
        """Retorna una lista de todos los objetos TipoIncidente."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM TIPO_INCIDENTE")
            tipos = [self.__row_to_tipo_incidente(row) for row in cursor.fetchall()]
            return tipos
        finally:
            conn.close()