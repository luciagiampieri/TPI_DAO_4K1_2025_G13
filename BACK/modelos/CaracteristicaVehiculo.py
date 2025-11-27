
class CaracteristicaVehiculo:
    
    def __init__(self, id_caracteristica, modelo, anio, categoria):
        self.id_caracteristica = id_caracteristica
        self.modelo = modelo
        self.anio = anio
        self.categoria = categoria


    def __str__(self):
        return f"Caracteristica Vehiculo: {self.modelo}, {self.anio}, {self.categoria}"