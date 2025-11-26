import sqlite3
from ...BACK.modelos import Ambito 
from db_conection import DBConnection


class AmbitoManager:
    """Clase DAO para manejar la persistencia de objetos Ambito."""
    
    def __init__(self):
        self.db_connection = DBConnection()


    def __row_to_ambito(self, row):
        """Mapea un registro (fila de la BD) a un objeto Ambito."""
        if row is None:
            return None
            
        return Ambito(
            id_ambito=row['ID_AMBITO'],
            ambito=row['TX_AMBITO'] # Usamos 'TX_AMBITO' según tu script SQL
        )


    # --- Método LEER (Consulta por ID) ---
    def obtener_por_id(self, id_ambito):
        """Busca un ámbito por su ID y retorna un objeto Ambito."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT ID_AMBITO, TX_AMBITO FROM AMBITO WHERE ID_AMBITO = ?", (id_ambito,))
            row = cursor.fetchone()
            
            # Usamos la función de mapeo interna
            return self.__row_to_ambito(row)
            
        except sqlite3.Error as e:
            print(f"Error al obtener ámbito: {e}")
            return None
        finally:
            conn.close()


    # --- Método LEER TODO (Listado) ---
    def listar_todos(self):
        """Retorna una lista de todos los objetos Ambito."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT ID_AMBITO, TX_AMBITO FROM AMBITO")
            
            # Mapeamos cada registro de la lista con la función interna
            ambitos = [self.__row_to_ambito(row) for row in cursor.fetchall()]
            return ambitos
        except sqlite3.Error as e:
            print(f"Error al listar ámbitos: {e}")
            return []
        finally:
            conn.close()