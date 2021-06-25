class Vacuna:
    """Clase para representar vacunas
    """
    def __init__(self, x, y, efectividad):
        """Constructor para vacunas

        Parámetros
        ----------
        x : int
            Coordenada x
        y : int
            Coordenada y
        efectividad : double
            Porcentaje de efectividad de la vacuna
        """
        self.x = x
        self.y = y
        self.efectividad = efectividad
