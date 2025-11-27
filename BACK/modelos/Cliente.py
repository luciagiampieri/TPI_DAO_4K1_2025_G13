class Cliente:
    
    def __init__(self, nombre, dni, telefono=None, mail=None, id_cliente=None):
        self.id_cliente = id_cliente 
        self.nombre = nombre
        self.dni = dni
        self.telefono = telefono
        self.mail = mail

    def __str__(self):
        return f"Cliente(ID: {self.id_cliente}, Nombre: {self.nombre}, DNI: {self.dni})"