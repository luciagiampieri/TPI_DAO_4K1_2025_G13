
class Mantenimiento:

    def __init__(self, id_mantenimiento, vehiculo, tipo_mantenimiento, fecha_inicio, fecha_fin, costo, observacion):
        self.id_mantenimiento = id_mantenimiento
        self.vehiculo = vehiculo
        self.tipo_mantenimiento = tipo_mantenimiento
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.costo = costo
        self.observacion = observacion


    def __str__(self):
        return f"Mantenimiento del Vehiculo: ({self.vehiculo}), Tipo Mantenimiento: {self.tipo_mantenimiento}, Fecha Inicio: {self.fecha_inicio}, Fecha Fin: {self.fecha_fin}, Costo: {self.costo}, Observacion: {self.observacion}"