
class Estado:
    
    def __init__(self, id_estado, ambito, estado):
        self.id_estado = id_estado
        self.ambito = ambito
        self.estado = estado

    
    def __str__(self):
        return f"Estado: {self.estado}, Ambito: {self.ambito}"