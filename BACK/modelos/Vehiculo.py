

class Vehiculo:

    def __init__(self, id_vehiculo, caracteristica_vehiculo, estado, patente, kilometraje, costo_diario):
        self.id_vehiculo = id_vehiculo
        self.caracteristica_vehiculo = caracteristica_vehiculo
        self.estado = estado
        self.patente = patente
        self.kilometraje = kilometraje
        self.costo_diario = costo_diario


    def setKilometraje(self, km):
        self.kilometraje = km


    def __str__(self):
        return f"Vehiculo ID: {self.id_vehiculo}, Caracteristicas: {self.caracteristica_vehiculo}, Estado: {self.estado}, Patente: {self.patente}, Kilometraje: {self.kilometraje}, Costo Diario: {self.costo_diario}"
        