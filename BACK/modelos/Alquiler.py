from .Estado import Estado
from .Vehiculo import Vehiculo

class Alquiler:

    def __init__(self, id_alquiler, vehiculo : Vehiculo, empleado, cliente, fecha_inicio, fecha_fin, costo_total, estado):
        self.id_alquiler = id_alquiler
        self.vehiculo = vehiculo
        self.empleado = empleado
        self.cliente = cliente
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.costo_total = costo_total
        self.estado = estado


    def calcular_costo(self):
        """Calcula el costo total del alquiler basado en la duración y el costo diario del vehículo."""
        if self.fecha_fin and self.fecha_inicio:
            dias_alquiler = (self.fecha_fin - self.fecha_inicio).days + 1
            self.costo_total = dias_alquiler * self.vehiculo.costo_diario
        else:
            self.costo_total = 0

    
    def finalizar_alquiler(self, km_final):
        """Finaliza el alquiler actualizando la fecha de fin y calculando el costo total."""
        from datetime import datetime
        self.fecha_fin = datetime.now()
        self.calcular_costo()
        self.estado = Estado(8, "Finalizado")  # Asumiendo 8 es el ID para 'Finalizado'
        # TODO pasar esto a patron state 

        # Actualizar el kilometraje del vehículo
        self.vehiculo.setKilometraje(km_final)

    
    def __str__(self):
        return f"Alquiler {self.id_alquiler}, Vehiculo: {self.vehiculo}, Cliente: {self.cliente}, Desde: {self.fecha_inicio}, Hasta: {self.fecha_fin}, Costo Total: {self.costo_total}"