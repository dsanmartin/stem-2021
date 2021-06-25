from math import inf
from persona import Persona
from vacuna import Vacuna
from random import randint, uniform
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Colores para estados de personas
COLORES = ['green', 'red', 'blue']

# Funcion de distancia
def distancia(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

class Simulacion:
    """
    Clase para controlar la simulación
    """
    def __init__(self, poblacion, vacunas, dias_simulacion, x_min, x_max, y_min, y_max, 
        porc_infectados=0.1, prob_vacuna=0.5):
        """Constructor de la simulación

        Parámetros
        ----------
        poblacion : int
            Número de personas en la simulación
        vacunas : int
            Número de vacunas en la simulación
        dias_simulacion : int
            Días de duración de simulación
        x_min : int
            Frontera izquierda del dominio
        x_max : int
            Frontera derecha del dominio
        y_min : int
            Frontera inferior del dominio
        y_max : int
            Frontera superior del dominio
        porc_infectados : float, opcional
            Porcentaje inicial de infectads, por default 0.1
        prob_vacuna : float, opcional
            Probabilidad de que una persona se vacune, by default 0.5
        """
        self.poblacion = poblacion
        self.dias_simulacion = dias_simulacion
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.porc_infectados = porc_infectados
        self.prob_vacuna = prob_vacuna # Probabilidad que una persona se vacune 
        self.personas = [] # Lista para guardar a las personas 
        self.vacunas = [] # Lista para guardar a las vacunas
        self.infectados = [] # Lista para guardar número de infectados por dia
        self.sanos = [] # Lista para guardar número de sanos por dia
        self.recuperados = [] # Lista para guardar número de recuperados diarios
        self.inoculados = [] # Lista para guardar el número de vacunados

        # Crear personas #
        for i in range(poblacion):
            # Posicion inicial aleatoria
            pos_x = randint(x_min, x_max)
            pos_y = randint(y_min, y_max)

            # Probabilidad de iniciar infectado
            if uniform(0, 1) < porc_infectados:
                estado = 1
            else:
                estado = 0

            # Creacion de persona. Inicia sin vacuna
            per = Persona(pos_x, pos_y, estado, False)

            # Agregamos a la lista
            self.personas.append(per)

        # Crear vacunas #
        for i in range(vacunas):
            # Posicion inicial aleatoria
            pos_x = randint(x_min, x_max)
            pos_y = randint(y_min, y_max)

            # Eficacia aleatoria entre 60% y 95%
            efect = uniform(0.6, 0.95) 

            # Creacion vacuna
            vac = Vacuna(pos_x, pos_y, efect)

            # Agregamos a la lista
            self.vacunas.append(vac)


    def mostrar_personas(self):
        """Mostrar informacion de personas
        """
        for persona in self.personas:
            persona.mostrar_persona()

    def mover_personas(self):
        """Simulación de movimiento de las personas
        """
        # Movimiento aleatorio de cada persona
        for persona in self.personas:
            # Movimiento aleatorio 
            persona.x += randint(-1, 1)
            persona.y += randint(-1, 1)

            # Condiciones periodicas
            persona.x %= self.x_max
            persona.y %= self.y_max

    def mover_vacunas(self):
        """Simulación de movimiento de las vacunas
        """
        # Movimiento de cada vacuna
        for vacuna in self.vacunas:
            # Movimiento aleatorio 
            vacuna.x += randint(-1, 1)
            vacuna.y += randint(-1, 1)

            # Condiciones periodicas
            vacuna.x %= self.x_max
            vacuna.y %= self.y_max

    def revisar_contagio(self, umbral=3.0):
        """Simular el contagio de personas.

        Parámetros
        ----------
        umbral : double, opcional
            Distancia umbral para contagio, por default 3.0
        """
        for i in range(self.poblacion):
            for j in range(self.poblacion):
                if i != j:
                    # Obtener informacion de las personas
                    x1 = self.personas[i].x
                    y1 = self.personas[i].y
                    x2 = self.personas[j].x
                    y2 = self.personas[j].y
                    estado1 = self.personas[i].estado
                    estado2 = self.personas[j].estado
                    # Para revisar el contagio se verifica:
                    # Si es que la persona está sana y hay una infectada cerca según el umbral
                    if distancia(x1, y1, x2, y2) <= umbral and estado1 == 0 and estado2 == 1:
                        # Efecto vacuna. Revisamos el % de inoculacion de la persona
                        # En el caso que no esté vacunado, la variable aleatoria será siempre <= 1, dado que inoculacion es 0
                        # En el caso que esté vacunado, la variable aletoria entra en juego y depende del % de inoculacion
                        if uniform(0, 1) <= 1 - self.personas[i].inoculacion:
                            self.personas[i].estado = 1 # Cambio a estado infectado

    def revisar_vacunacion(self, umbral=1.0):
        """Simular el proceso de vacunación.

        Parámetros
        ----------
        umbral : double, optional
            Distancia umbral para vacunación, por default 1.0
        """
        for persona in self.personas:
            for vacuna in self.vacunas:
                x1 = persona.x
                y1 = persona.y
                x2 = vacuna.x
                y2 = vacuna.y
                # El supuesto es que cada persona cerca del umbral de una vacuna será inoculada 
                # con probabilidad prob_vacuna, siempre y cuando su % de inoculacion sea nulo
                if distancia(x1, y1, x2, y2) <= umbral and persona.inoculacion == 0 and uniform(0, 1) <= self.prob_vacuna:
                    persona.inoculacion += vacuna.efectividad

    def estadisticas(self):
        """Obtención de estadísticas y actualización de estados
        """
        infectados = 0
        recuperados = 0
        inoculados = 0
        for persona in self.personas:
            # Revisar estado de personas
            if persona.estado == 1:
                infectados += 1
                if persona.dias_enfermo > 0:
                    persona.dias_enfermo -= 1
                    if persona.dias_enfermo == 0:
                        persona.estado = 2
            elif persona.estado == 2:
                recuperados += 1
            
            # Si la persona tiene vacuna
            if persona.inoculacion > 0:
                inoculados += 1
        # Cálculo de personas sanas
        sanos = self.poblacion - infectados - recuperados
        # Agregar estadisticas
        self.infectados.append(infectados)
        self.sanos.append(sanos)
        self.recuperados.append(recuperados)
        self.inoculados.append(inoculados)

    def plot(self):
        """Gráfico de movimientos y estadísticas
        """
        # Estructuras para personas
        colores = []
        coors_x_per = []
        coors_y_per = []
        # Estructura para vacunas
        coors_x_vac = []
        coors_y_vac = []
        # Información de personas
        for persona in self.personas:
            # Pintamos cyan las personas que no estén infectas e inoculadas
            if persona.inoculacion > 0 and persona.estado != 1:
                colores.append('cyan')
            else: # Pintamos según su estado
                colores.append(COLORES[persona.estado])
            coors_x_per.append(persona.x)
            coors_y_per.append(persona.y)
        # Información de vaunas
        for vacuna in self.vacunas:
            coors_x_vac.append(vacuna.x)
            coors_y_vac.append(vacuna.y)

        fig = plt.figure(figsize=(12, 4))

        # Gráfico izquierdo. Personas y vacunas
        ax1 = fig.add_subplot(121)
        per_sc = ax1.scatter(coors_x_per, coors_y_per, c=colores, label=colores)
        vac_sc = ax1.scatter(coors_x_vac, coors_y_vac, c='orange', marker='X')
        ax1.set_xlim([self.x_min, self.x_max])
        ax1.set_ylim([self.y_min, self.y_max])
        
        # Leyenda de scatter
        handles_ = [
            mpatches.Patch(color='green', label='Sano'),
            mpatches.Patch(color='red', label='Infectado'),
            mpatches.Patch(color='blue', label='Recuperado'),
            mpatches.Patch(color='cyan', label='Vacunado'),
            mpatches.Patch(color='orange', label='Vacuna')
        ]
        ax1.legend(handles=handles_, loc='upper right', bbox_to_anchor=(1.1, 1.1), fancybox=True)

        # Gráfico derecho. Estadísticas
        ax2 = fig.add_subplot(122)
        ax2.set_title("Infectados: " + str(self.infectados[-1]) + " - Sanos: " + str(self.sanos[-1]) + 
            " - Recuperados: " + str(self.recuperados[-1]) + " - Inoculados: " + str(self.inoculados[-1]))
        t = list(range(len(self.infectados)))
        ax2.plot(t, self.infectados, 'r-x', label="Infectados")
        ax2.plot(t, self.sanos, 'g-o', label="Sanos")
        ax2.plot(t, self.recuperados, 'b-d', label="Recuperados")
        ax2.plot(t, self.inoculados, 'c-s', label="Inoculados")
        ax2.set_xlabel("t")
        ax2.set_ylabel("#")
        ax2.legend(loc='upper left', fancybox=True)
        plt.show()

    def ejecutar(self):
        """Ejecutar la simulación.
        """
        d = 0 # Contador de dias
        while d <= self.dias_simulacion:
            self.mover_personas()
            self.revisar_contagio()
            self.mover_vacunas()
            self.revisar_vacunacion()
            self.estadisticas()
            self.plot()
            d += 1
            # Detener la simulación cuando ya estén todos recuperados
            if self.recuperados[-1] == self.poblacion: 
                d = self.dias_simulacion + 1



    

