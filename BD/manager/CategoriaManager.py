import sqlite3
from BACK.modelos import Categoria 
from ..db_conection import DBConnection

class CategoriaManager:
    def __init__(self):
        self.db_connection = DBConnection()


    def __row_to_categoria(self, row):
        """Mapea un registro a un objeto Categoria."""
        if row is None:
            return None
        return Categoria(
            id_categoria=row['ID_CATEGORIA'],
            categoria=row['TX_CATEGORIA'] # Usamos 'TX_CATEGORIA' según tu script SQL
        )


    def obtener_por_id(self, id_categoria):
        """Busca una categoría por su ID."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT ID_CATEGORIA, TX_CATEGORIA FROM CATEGORIA WHERE ID_CATEGORIA = ?", (id_categoria,))
            row = cursor.fetchone()
            return self.__row_to_categoria(row)
        except sqlite3.Error as e:
            print(f"Error al obtener categoría: {e}")
            return None
        finally:
            conn.close()


    def listar_todos(self):
        """Retorna una lista de todos los objetos Categoria."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT ID_CATEGORIA, TX_CATEGORIA FROM CATEGORIA")
            categorias = [self.__row_to_categoria(row) for row in cursor.fetchall()]
            return categorias
        except sqlite3.Error as e:
            print(f"Error al listar categorías: {e}")
            return []
        finally:
            conn.close()