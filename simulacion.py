from persona import Persona
from random import randint, uniform
import matplotlib.pyplot as plt

COLORES = ['green', 'red', 'blue']

def distancia(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

class Simulacion:
    """
    Clase para controlar la simulación
    """
    def __init__(self, poblacion, dias_simulacion, x_min, x_max, y_min, y_max, 
        porcentaje_infectados=0.1, eficacia_vacuna=0.8, dias_incubacion=14):
        self.poblacion = poblacion
        self.dias_simulacion = dias_simulacion
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.porcentaje_infectados = porcentaje_infectados
        self.eficacia_vacuna = eficacia_vacuna
        self.personas = [] # Lista para guardar a las personas 
        self.infectados = [] # Lista para guardar número de infectados por dia
        self.sanos = [] # Lista para guardar número de sanos por dia
        self.recuperados = [] # Lista para guardar número de recuperados diarios

        # Crear personas #
        for i in range(poblacion):
            # Posicion inicial aleatoria
            pos_x = randint(x_min, x_max)
            pos_y = randint(y_min, y_max)

            # Probabilidad de iniciar infectado
            if uniform(0, 1) < porcentaje_infectados:
                estado = 1
            else:
                estado = 0

            # Creacion de persona. Inicia sin vacuna
            per = Persona(pos_x, pos_y, estado, False)

            # Agregamos a la lista
            self.personas.append(per)

    def obtener_personas(self):
        return self.personas

    def mostrar_personas(self):
        for persona in self.personas:
            persona.mostrar_persona()

    def mover(self):
        for persona in self.personas:
            # Movimiento aleatorio 
            persona.x += randint(-1, 1)
            persona.y += randint(-1, 1)

            # Condiciones periodicas
            persona.x %= self.x_max
            persona.y %= self.y_max

    def revisar_contagio(self, umbral=3):
        for i in range(self.poblacion):
            for j in range(self.poblacion):
                if i != j:
                    x1 = self.personas[i].x
                    y1 = self.personas[i].y
                    x2 = self.personas[j].x
                    y2 = self.personas[j].y
                    estado1 = self.personas[i].estado
                    estado2 = self.personas[j].estado
                    if distancia(x1, y1, x2, y2) <= umbral and estado1 == 0 and estado2 == 1:
                        if self.personas[i].vacuna: # Efecto vacuna
                            if uniform(0, 1) <= 1 - self.eficacia_vacuna:
                                self.personas[i].estado = 1
                        else:
                            self.personas[i].estado = 1


    def estadisticas(self):
        infectados = 0
        recuperados = 0
        for persona in self.personas:
            if persona.estado == 1:
                infectados += 1
                if persona.dias_enfermo > 0:
                    persona.dias_enfermo -= 1
                    if persona.dias_enfermo == 0:
                        persona.estado = 2
            elif persona.estado == 2:
                recuperados += 1
        sanos = self.poblacion - infectados - recuperados
        #print("Infectados: %d, sanos: %d, recuperdos: %d" % (infectados, sanos, recuperados))
        self.infectados.append(infectados)
        self.sanos.append(sanos)
        self.recuperados.append(recuperados)

    def plot(self):
        colores = []
        coors_x = []
        coors_y = []
        for persona in self.personas:
            colores.append(COLORES[persona.estado])
            coors_x.append(persona.x)
            coors_y.append(persona.y)

        fig = plt.figure(figsize=(12, 4))
        ax1 = fig.add_subplot(121)

        ax1.scatter(coors_x, coors_y, c=colores)
        ax1.set_xlim([self.x_min, self.x_max])
        ax1.set_ylim([self.y_min, self.y_max])

        ax2 = fig.add_subplot(122)
        ax2.set_title("Infectados: " + str(self.infectados[-1]) + " - Sanos: " + str(self.sanos[-1]) + " - Recuperados: " + str(self.recuperados[-1]))
        t = list(range(1, len(self.infectados) + 1))
        # s = self.infectados
        # h = self.sanos
        ax2.plot(t, self.infectados, 'r', label="Infectados")
        ax2.plot(t, self.sanos, 'g', label="Sanos")
        ax2.plot(t, self.recuperados, 'b', label="Recuperados")
        ax2.set_xlabel("t")
        ax2.set_ylabel("#")
        ax2.grid(True)
        ax2.legend()

        plt.show()

    def ejecutar(self):
        d = 0
        while d <= self.dias_simulacion:
            self.mover()
            self.revisar_contagio()
            self.estadisticas()
            self.plot()
            d += 1

            if self.recuperados[-1] == self.poblacion: # Ya se recuperaron todos
                d = self.dias_simulacion + 1



    

