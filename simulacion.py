class Simulacion:
    """
    Clase para controlar la simulación
    """
    def __init__(self, poblacion, dias_simulacion, x_min, x_max, y_min, y_max, 
        porcentaje_infectados=0.1, dias_incubacion=14):
        self.poblacion = poblacion
        self.dias_simulacion = dias_simulacion
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.porcentaje_infectados = porcentaje_infectados
