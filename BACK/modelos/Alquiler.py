
class Alquiler:

    def __init__(self, id_alquiler, vehiculo, empleado, cliente, fecha_inicio, fecha_fin, costo_total, estado):
        self.id_alquiler = id_alquiler
        self.vehiculo = vehiculo
        self.empleado = empleado
        self.cliente = cliente
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.costo_total = costo_total
        self.estado = estado

    
    def __str__(self):
        return f"Alquiler {self.id_alquiler}, Vehiculo: {self.vehiculo}, Cliente: {self.cliente}, Desde: {self.fecha_inicio}, Hasta: {self.fecha_fin}, Costo Total: {self.costo_total}"