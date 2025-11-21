import sqlite3
from BACK.modelos import Estado
from db_conection import DBConnection
from AmbitoManager import AmbitoManager 

class EstadoManager:
    """Clase Manager para manejar la persistencia de objetos Estado."""
    
    def __init__(self):
        self.db_connection = DBConnection()
        self.ambito_dao = AmbitoManager() # Dependencia inyectada (o creada)

    def __row_to_estado(self, row):
        """Mapea un registro (fila de la BD) a un objeto Estado, resolviendo la dependencia Ambito."""
        if row is None:
            return None
            
        # 1. Resolver la dependencia: Obtener el objeto Ambito
        ambito_obj = self.ambito_dao.obtener_por_id(row['ID_AMBITO'])
        
        # 2. Crear y retornar el objeto Estado
        return Estado(
            id_estado=row['ID_ESTADO'],
            estado=row['TX_ESTADO'], # Usamos TX_ESTADO según tu script SQL
            ambito=ambito_obj
        )

    # --- Método LEER (Consulta por ID) ---
    def obtener_por_id(self, id_estado):
        """Busca un estado por su ID y retorna un objeto Estado."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            # Seleccionamos las columnas necesarias para el mapeo
            cursor.execute("SELECT ID_ESTADO, TX_ESTADO, ID_AMBITO FROM ESTADO WHERE ID_ESTADO = ?", (id_estado,))
            row = cursor.fetchone()
            
            return self.__row_to_estado(row)
            
        except sqlite3.Error as e:
            print(f"Error al obtener estado: {e}")
            return None
        finally:
            conn.close()

    # --- Método LEER TODO (Listado) ---
    def listar_todos(self):
        """Retorna una lista de todos los objetos Estado."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT ID_ESTADO, TX_ESTADO, ID_AMBITO FROM ESTADO")
            
            estados = [self.__row_to_estado(row) for row in cursor.fetchall()]
            return estados
        except sqlite3.Error as e:
            print(f"Error al listar estados: {e}")
            return []
        finally:
            conn.close()