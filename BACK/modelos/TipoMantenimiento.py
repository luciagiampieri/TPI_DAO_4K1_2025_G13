
class TipoMantenimiento:
    def __init__(self, id_tipo_mantenimiento, tipo_mantenimiento):
        self.id_tipo_mantenimiento = id_tipo_mantenimiento
        self.tipo_mantenimiento = tipo_mantenimiento

    
    def __str__(self):
        return f"Tipo Mantenimiento: {self.tipo_mantenimiento}"