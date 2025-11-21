
class Incidente:

    def __init__(self, id_incidente, tipo_incidente, alquiler, fecha_incidente, descripcion, costo):
        self.id_incidente = id_incidente
        self.tipo_incidente = tipo_incidente
        self.alquiler = alquiler
        self.fecha_incidente = fecha_incidente
        self.descripcion = descripcion
        self.costo = costo

    def __str__(self):
        return f"Incidente {self.id_incidente}, Tipo: {self.tipo_incidente}, Fecha: {self.fecha_incidente}, Alquiler: {self.alquiler}, Costo: {self.costo}"