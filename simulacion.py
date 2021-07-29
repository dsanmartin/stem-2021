from persona import Persona
from vacuna import Vacuna
from random import randint, uniform, seed

# Semilla para la generacion de numeros aleatorios
seed(12345)

# Funcion de distancia
def distancia(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

class Simulacion:
    """Clase para controlar la simulación"""

    def __init__(self, poblacion, vacunas, dias_simulacion, x_min, x_max, y_min, y_max, 
        porc_infectados=0.1, prob_vacuna=0.5, prob_reb=0.5):
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
            Porcentaje inicial de infectads, por omisión 10%
        prob_vacuna : float, opcional
            Probabilidad de que una persona se vacune, por omisión 50%
        prob_reb : float, opcional
            Probabilidad de rebrote, por omisión 50%
        """
        self.poblacion = poblacion
        self.dias_simulacion = dias_simulacion
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.porc_infectados = porc_infectados
        self.prob_vacuna = prob_vacuna # Probabilidad que una persona se vacune 
        self.prob_reb = prob_reb # Probabilidad de rebrote
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
        """Mostrar informacion de personas"""
        for persona in self.personas:
            persona.mostrar_persona()

    def revisar_colision(self, x, y, umbral):
        """Revisar si existen colisiones entre las personas y la posición (x, y).

        Parámetros
        ----------
        x : int
            Coordenada x
        y : int
            Coordenada y
        umbral : float
            Umbral para revisar la colisión

        Retorna
        -------
        boolean
            Devuelve verdadero si existen colisiones y falso en caso contrario
        """
        for persona in self.personas:
            if distancia(x, y, persona.x, persona.y) <= umbral:
                return True
        return False

    def mover_personas(self, vel=5, umbral=5):
        """Simulación de movimiento de las personas

        Parámetros
        ----------
        mov : int, optional
            Distancia de movimiento, por omisión 5
        """
        # Movimiento aleatorio de cada persona
        # Este while permite que el programa principal espere que la función se termine de ejecutar
        while True:
            for persona in self.personas:
                # Bandera para verificar que cada persona asegure una posicion nueva sin colisión
                flag = True
                # Se genera un movimiento aleatorio siempre y cuando no exista colisión
                while flag: 
                    # Movimiento aleatorio 
                    tmp_x = persona.x + randint(-vel, vel)
                    tmp_y = persona.y + randint(-vel, vel)

                    # Condiciones periodicas
                    tmp_x %= self.x_max
                    tmp_y %= self.y_max

                    # Verificar si existe colisión con la nueva posición, 
                    # en caso contrario volver a generar una nueva
                    if not self.revisar_colision(tmp_x, tmp_y, umbral):
                        flag = False
                        persona.x = tmp_x
                        persona.y = tmp_y
            
            # Se cierra el ciclo para seguir la ejecución del programa principal
            break 

    def mover_vacunas(self, vel=5):
        """Simulación de movimiento de las vacunas

        Parámetros
        ----------
        mov : int, optional
            Distancia de movimiento, por omisión 5
        """
        # Movimiento de cada vacuna
        for vacuna in self.vacunas:
            # Movimiento aleatorio 
            vacuna.x += randint(-vel, vel)
            vacuna.y += randint(-vel, vel)

            # Condiciones periodicas
            vacuna.x %= self.x_max
            vacuna.y %= self.y_max

    def revisar_contagio(self, umbral=10.0):
        """Simular el contagio de personas.

        Parámetros
        ----------
        umbral : double, opcional
            Distancia umbral para contagio, por omisión 10.0
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

    def revisar_vacunacion(self, umbral=10.0):
        """Simular el proceso de vacunación.

        Parámetros
        ----------
        umbral : double, optional
            Distancia umbral para vacunación, por omisión 10.0
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

    def rebrote(self, porc=0.02):
        """Simular rebrote de virus
        
        Parametros
        ----------
        porc : double, opcional
            Porcentaje de rebrote, por omisión 5%
        """
        k = 0
        for persona in self.personas:
            if persona.estado == 0 and persona.inoculacion == 0 and k < self.poblacion * porc:
                persona.estado = 1 # Infectado
                persona.dias_enfermo = randint(28, 50) # Nuevos días enfermo
                k += 1
    
    def estadisticas(self):
        """Obtención de estadísticas y actualización de estados"""
        # Contadores
        sanos = 0
        infectados = 0
        recuperados = 0
        inoculados = 0
        for persona in self.personas:
            # Revisar estado de personas
            if persona.estado == 0: # Sano
                sanos += 1
            elif persona.estado == 1: # Infectado
                infectados += 1
                if persona.dias_enfermo > 0:
                    persona.dias_enfermo -= 1
                    if persona.dias_enfermo == 0: # Si ya terminó los días enfermos
                        persona.estado = 2 # Recuperado
            elif persona.estado == 2: # Recuperado
                recuperados += 1
            # Si la persona tiene vacuna
            if persona.inoculacion > 0:
                inoculados += 1
        # Agregar estadisticas
        self.infectados.append(infectados)
        self.sanos.append(sanos)
        self.recuperados.append(recuperados)
        self.inoculados.append(inoculados)
        # Rebrote
        if infectados == 0 and uniform(0, 1) <= self.prob_reb:
            self.rebrote()

