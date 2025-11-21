
class Categoria:

    def __init__(self, id_categoria, categoria):
        self.id_categoria = id_categoria
        self.categoria = categoria

    
    def __str__(self):
        return f"Categoria: {self.categoria}"