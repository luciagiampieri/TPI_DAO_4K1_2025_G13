from BD.manager.ReporteManager import ReporteManager

class GestorReportes:
    def __init__(self):
        # Instanciamos el manager de BD que creamos antes
        self.reporte_manager = ReporteManager()

    def obtener_ranking_vehiculos(self):
        # Aquí podrías agregar lógica extra si fuera necesaria (ej: formatear datos)
        return self.reporte_manager.obtener_ranking_vehiculos()

    def obtener_facturacion_anual(self, anio):
        return self.reporte_manager.obtener_facturacion_mensual(anio)

    def obtener_reporte_periodo(self, f_desde, f_hasta):
        return self.reporte_manager.alquileres_por_periodo(f_desde, f_hasta)
    
    def obtener_historial_cliente(self, id_cliente):
        return self.reporte_manager.historial_cliente_detallado(id_cliente)