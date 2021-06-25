from random import randint

class Persona:
    """Clase para representar a una persona
    """

    def __init__(self, x, y, estado, vacuna):
        """ Constructor Persona
        
        Parámetros
        ----------
        x : double
            Coordenada x
        y : double
            coordenada y
        estado : int
            Estado de la persona: 
            * 0: sano
            * 1: infectado
            * 2: recuperado
        vacuna : boolean
            Estado de vacuna
        """
        self.x = x
        self.y = y
        self.estado = estado
        self.vacuna = vacuna
        self.dias_enfermo = randint(7, 25) # Duracion enfemerdad entre 7 y 25 dias
        self.inoculacion = 0 # Porcentaje de inoculacion de persona

    def mostrar_persona(self):
        estados = ["no infectado", "infectado", "recuperado"]
        print("Estoy en la posicion: (%d, %d)" % (self.x, self.y))
        print("Mi estado es: %s" % (estados[self.estado]))
        if self.vacuna:
            print("Estoy vacunado")
        else:
            print("No estoy vacunado")
        print()