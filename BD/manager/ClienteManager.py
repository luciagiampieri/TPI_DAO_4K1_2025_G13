import sqlite3
from ...BACK.modelos import Cliente
from db_conection import DBConnection

class ClienteManager:
    """Clase Manager para manejar la persistencia de objetos Cliente."""
    def __init__(self):
        self.db_connection = DBConnection()

    # --- Función privada para el mapeo (solo accesible dentro del Manager) ---
    def __row_to_cliente(self, row):
        """Mapea un registro (fila de la BD) a un objeto Cliente."""
        if row is None:
            return None
            
        return Cliente(
            id_cliente=row['ID_CLIENTE'],
            nombre=row['NOMBRE'],
            dni=row['DNI'],
            telefono=row['TELEFONO'],
            mail=row['MAIL']
        )
        

    # --- 1. Método CREAR (Alta) ---
    def guardar(self, cliente):
        """Guarda un nuevo cliente en la base de datos."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO CLIENTE (NOMBRE, DNI, TELEFONO, MAIL) 
                VALUES (?, ?, ?, ?)
            """, (cliente.nombre, cliente.dni, cliente.telefono, cliente.mail))
            
            cliente.id_cliente = cursor.lastrowid
            conn.commit()
            return cliente
        except sqlite3.IntegrityError:
            print(f"Error: Ya existe un cliente con el DNI {cliente.dni}.")
            return None
        except sqlite3.Error as e:
            print(f"Error al guardar el cliente: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()


    # --- 2. Método LEER (Consulta por ID) ---
    def obtener_por_id(self, id_cliente):
        """Busca un cliente por su ID y retorna un objeto Cliente."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM CLIENTE WHERE ID_CLIENTE = ?", (id_cliente,))
            row = cursor.fetchone()
            
            # ¡Aquí usamos la función de mapeo interna!
            return self.__row_to_cliente(row)
            
        except sqlite3.Error as e:
            print(f"Error al obtener cliente: {e}")
            return None
        finally:
            conn.close()


    # --- 3. Método LEER TODO (Listado) ---
    def listar_todos(self):
        """Retorna una lista de todos los objetos Cliente."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM CLIENTE")
            
            # Mapeamos cada registro de la lista con la función interna
            clientes = [self.__row_to_cliente(row) for row in cursor.fetchall()]
            return clientes
        except sqlite3.Error as e:
            print(f"Error al listar clientes: {e}")
            return []
        finally:
            conn.close()
            

    # --- 4. Método ACTUALIZAR (Modificación)
    def actualizar(self, cliente):
        """Actualiza los datos de un cliente existente."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE CLIENTE 
                SET NOMBRE = ?, DNI = ?, TELEFONO = ?, MAIL = ? 
                WHERE ID_CLIENTE = ?
            """, (cliente.nombre, cliente.dni, cliente.telefono, cliente.mail, cliente.id_cliente))
            
            conn.commit()
            return cursor.rowcount > 0  # Retorna True si se actualizó algún registro
        except sqlite3.IntegrityError:
            print(f"Error: Ya existe un cliente con el DNI {cliente.dni}.")
            return False
        except sqlite3.Error as e:
            print(f"Error al actualizar el cliente: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    