
class Empleado:

    def __init__(self, id_empleado, nombre, dni, mail):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.dni = dni
        self.mail = mail

    
    def __str__(self):
        return f"Empleado: {self.nombre}, DNI: {self.dni}, Mail: {self.mail}"