
class TipoIncidente:

    def __init__(self, id_tipo_incidente, tipo_incidente):
        self.id_tipo_incidente = id_tipo_incidente
        self.tipo_incidente = tipo_incidente

    
    def __str__(self):
        return f"Tipo Incidente: {self.tipo_incidente}"