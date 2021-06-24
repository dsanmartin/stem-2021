class Persona:
    """
    Clase para representar a una persona
    
    """

    def __init__(self, x, y, estado, vacuna):
        """
        Parámetros
        ----------
        x : double
            Coordenada x
        y : double
            coordenada y
        estado : int
            Estado de la persona: 
            * 0: no infectado
            * 1: infectado
        vacuna : boolean
            Estado de vacuna
        """
        self.x = x
        self.y = y
        self.estado = estado
        self.vacuna = vacuna

    def pos_x(self):
        return self.x

    def pos_y(self):
        return self.y
    
    def obtener_estado(self):
        return self.estado

    def obtener_vacuna(self):
        return self.vacuna

    def modificar_x(self, x):
        self.x = x

    def modificar_y(self, y):
        self.y = y

    def modificar_estado(self, estado):
        self.estado = estado

    def modificar_vacuna(self, vacuna):
        self.vacuna = vacuna