import sys
import pygame
from pygame.locals import *
from simulacion import Simulacion

# Colores utilizados en el juego #
NEGRO    = (0, 0, 0)
BLANCO   = (255, 255, 255)
ROJO     = (255, 0, 0)
VERDE    = (0, 255, 0)
AZUL     = (0, 0, 255)
CYAN     = (0, 255, 255)

# Colores para estados de personas #
COLORES = [VERDE, ROJO, AZUL]

# Información fondo del juego
PIX = 32 # Pixeles baldosas
N_BALD_X = 25 # Número baldosas eje x
N_BALD_Y = 15 # Número baldosas eje y

# Area de juego #
XMIN = 20 
XMAX = PIX * N_BALD_X + XMIN
YMIN = 20
YMAX = PIX * N_BALD_Y + YMIN
ANCHO = XMAX - XMIN
ALTO = YMAX - YMIN
 
# Frames por segundo #
FPS = 5

# Radio de círculo #
RADIO = 5

# Imágenes #
VACIMG = pygame.image.load('img/vaccine.png') # Vacuna
PERIMG = pygame.image.load('img/person.png') # Personas
BALDO = pygame.image.load('img/tile.png') # Baldosas

def colorear(imagen, color):
    """Crea una copia de la imagen con el color especificado.

    Parámetros
    ----------
    imagen : Imagen de Pygame
        Imagen a colorear
    color : Color de Pygame
        Color utilizado para colorear la imagen

    Retorna
    -------
    Imagen de Pygame
        Nueva imagen coloreada
    """
    imagen = imagen.copy() # Copia de la imagen
    imagen.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT) # Eliminar los colores de la imagen
    imagen.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD) # Colorear la imagen
    return imagen


def revisar_final():
    """Revisa si el juego se cierra.
    """
    for event in pygame.event.get(QUIT): # Obtener todos los eventos de tipo QUIT (cerrar)
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP): # Obtener todos los eventos de tipo KEYUP (tecleo)
        if event.key == K_ESCAPE: # Terminar si se presiona ESCAPE
            pygame.quit()
            sys.exit()
        pygame.event.post(event)

def pos(x, y):
    """Coordenadas de plano cartesiano a coordenadas de pygame.

    Parámetros
    ----------
    x : int
        Coordenadas x en plano cartesiano.
    y : int
        Coordenadas y en plano cartesiano.

    Retorna
    -------
    tuple
        Retorna la posición en coordenadas de Pygame
    """
    return (XMIN + x, YMAX - y)

def dibujar_vacuna(display, posicion):
    """Dibuja la vacuna en la posición especificada.

    Parámetros
    ----------
    display : Pantalla de Pygame
        Pantalla donde se dibujará la vacuna
    posicion : tuple
        Posición donde se dibujará la vacuna
    """
    display.blit(VACIMG, posicion)

def dibujar_persona(display, posicion, color):
    """Dibuja la persona en la posición especificada y color definido.

    Parámetros
    ----------
    display : Pantalla de Pygame
        Pantalla donde se dibujará la persona
    posicion : tuple
        Posición donde se dibujará la persona
    color : Color de Pygame
        Color utilizado para colorear a la persona
    """
    display.blit(colorear(PERIMG, color), posicion)

def dibujar_baldosas(display):
    """Dibuja las baldosas en la pantalla.

    Parámetros
    ----------
    display : Pantalla de Pygame
        Pantalla donde se dibujarán las baldosas
    """
    fil = ALTO // PIX + 1 # Número de filas
    col = ANCHO // PIX # Número de columnas
    posy = 0
    # Dibujar las baldosas en el área de juego
    for i in range(fil):
        posx = 0
        for j in range(col):
            display.blit(BALDO, (posx + XMIN, posy + YMIN))
            posx += PIX
        posy += PIX

def plot(display, personas, vacunas):
    """Dibujar los agentes de la simulación.

    Parámetros
    ----------
    display : Pantalla de Pygame
        Pantalla donde se dibujarán los agentes
    personas : list
        Lista de personas
    vacunas : list
        Lista de vacunas
    """
    # Dibujar personas
    for persona in personas:
        if persona.inoculacion > 0 and persona.estado != 1: # Persona vacunada
            dibujar_persona(display, pos(persona.x, persona.y), CYAN) 
        else:
            dibujar_persona(display, pos(persona.x, persona.y), COLORES[persona.estado])
    # Dibujar vacunas
    for vacuna in vacunas:
        dibujar_vacuna(display, pos(vacuna.x, vacuna.y))

def contador(display, sim, d):
    """Generar el contador con estadísticas

    Parámetros
    ----------
    display : Pantalla de Pygame
        Pantalla donde se dibujará el contador
    sim : Simulacion
        Objeto simulación con toda la información necesaria
    """
    # Fuentes utilizadas
    font_1 = pygame.font.SysFont("Arial", 11, bold=True)
    font_2 = pygame.font.SysFont("Arial", 12)
    # Marco
    pygame.draw.rect(display, NEGRO, pygame.Rect(XMAX + 25, YMIN , 120, 100), width=1)
    # Titulo
    titulo = font_1.render("CONTADOR", 1, NEGRO)
    display.blit(titulo, (XMAX + 27, YMIN))
    # Etiquetas personas
    pygame.draw.circle(display, VERDE, (XMAX + 35, YMIN + 22), RADIO) # Sano
    pygame.draw.circle(display, ROJO, (XMAX + 35, YMIN + 42), RADIO) # Infectado
    pygame.draw.circle(display, AZUL, (XMAX + 35, YMIN + 62), RADIO) # Recuperado
    pygame.draw.circle(display, CYAN, (XMAX + 35, YMIN + 82), RADIO) # Vacunado
    # Estadísticas
    n_sanos = sim.sanos[-1] if len(sim.sanos) > 0 else 0
    n_infec = sim.infectados[-1] if len(sim.infectados) > 0 else 0
    n_recup = sim.recuperados[-1] if len(sim.recuperados) > 0 else 0
    n_vacun = sim.inoculados[-1] if len(sim.inoculados) > 0 else 0
    # Texto
    label = font_2.render("Sanos " + str(n_sanos), 1, NEGRO)
    display.blit(label, (XMAX + 42, YMIN + 16))
    label = font_2.render("Infectados " + str(n_infec), 1, NEGRO)
    display.blit(label, (XMAX + 42, YMIN + 36))
    label = font_2.render("Recuperados " + str(n_recup), 1, NEGRO)
    display.blit(label, (XMAX + 42, YMIN + 56))
    label = font_2.render("Vacunados " + str(n_vacun), 1, NEGRO)
    display.blit(label, (XMAX + 42, YMIN + 76))
    # Días de simulación
    label = font_2.render("Día: " + str(d / 2), 1, NEGRO)
    display.blit(label, (XMAX + 42, YMIN + 100))

# Función principal #
def main():
    global FPSCLOCK, DISPLAY, BASICFONT # Variables de PyGame
    game_over = False # Variable para terminar el juego

    # Configuración PyGame #
    pygame.init() 
    FPSCLOCK = pygame.time.Clock() # Reloj del juego
    DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Configurar pantalla
    BASICFONT = pygame.font.Font('freesansbold.ttf', 16) # Tipografía
    pygame.display.set_caption('Videojuégatela por la Inmunidad - STEM 2021') # Título de la ventana

    # Personas en la simulacion
    poblacion = 100
    # Vacunas disponible en el juego
    vacunas = 1
    # Dias de simulacion
    dias_simulacion = 2000
    # Tamaño del "mundo" en plano cartesiano
    x_min = 0
    x_max = ANCHO - 12 # Ancho del juego - corrección tamaño de persona
    y_min = 0
    y_max = ALTO - 5
    # Porcentaje inicial de infectados
    porcentaje_infectados = 0.25
    # Probabilidad de que una persona se vacune
    probabilidad_vacuna = 1
    # Probabilidad de rebrote
    probabilidad_rebrote = 0.5
    # Velocidad de movimiento personas (pixeles / tick)
    vel_per = 10
    # Velocidad de movimiento vacunas (pixeles / tick)
    vel_vac = 10
    # Umbral colision
    umb_col = vel_per + 1
    # Umbral contagio
    umb_con = vel_per + 5
    # Umbral vacuna
    umb_vac = vel_vac + 5
    # Objeto de simulación
    sim = Simulacion(poblacion, vacunas, dias_simulacion, x_min, x_max, y_min, y_max, 
        porc_infectados=porcentaje_infectados, prob_vacuna=probabilidad_vacuna, prob_reb=probabilidad_rebrote)
    # 12 horas de simulacion
    d = 0 
    # Posicion inicial vacuna 
    sim.vacunas[0].x = x_max // 2
    sim.vacunas[0].y = y_max // 2

    # Ciclo principal del juego. 
    while not game_over:

        # Pantalla blanca
        DISPLAY.fill(BLANCO)

        # Dibujar el fondo con baldosas
        dibujar_baldosas(DISPLAY)

        # Contador estadísticas
        contador(DISPLAY, sim, d)

        # Revisar si se cierra el juego #
        revisar_final()

        # Consultar eventos de pygame (clic o teclas) #
        for event in pygame.event.get():
            # Mover la vacuna utilizando el mouse
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                # Validar que el clic se realice en el área de juego
                if mousex >= XMIN and mousex <= XMAX and mousey >= YMIN and mousey <= YMAX:
                    sim.vacunas[0].x = mousex - XMIN
                    sim.vacunas[0].y = YMAX - mousey
            # Mover vacuna utilizando el teclado
            elif event.type == KEYDOWN:
                if event.key == pygame.K_LEFT: # Tecla izquierda
                    sim.vacunas[0].x -= vel_vac # Mover vacuna a la izquierda
                    sim.vacunas[0].x %= sim.x_max # Restringir la posición a los límites del mundo
                elif event.key == pygame.K_RIGHT: # Tecla derecha
                    sim.vacunas[0].x += vel_vac # Mover vacuna a la derecha
                    sim.vacunas[0].x %= sim.x_max # Restringir la posición a los límites del mundo
                elif event.key == pygame.K_UP: # Tecla arriba
                    sim.vacunas[0].y += vel_vac # Mover vacuna arriba
                    sim.vacunas[0].y %= sim.y_max # Restringir la posición a los límites del mundo
                elif event.key == pygame.K_DOWN: # Tecla abajo
                    sim.vacunas[0].y -= vel_vac # Mover vacuna abajo
                    sim.vacunas[0].y %= sim.y_max # Restringir la posición a los límites del mundo

        # Etapas de simulación #
        sim.mover_personas(vel_per, umb_col) # Movimiento aleatorio de personas
        sim.revisar_contagio(umb_con) # Simular el contagio
        sim.revisar_vacunacion(umb_vac) # Simular el proceso de vacunación
        sim.estadisticas() # Obtención de estadísticas
        plot(DISPLAY, sim.personas, sim.vacunas) # Dibujar a los agentes
        d += 1 # Siguientes 12 horas de simulación

        # Detener la simulación cuando se alcancen los días definidos o ya estén todos recuperados
        if d == sim.dias_simulacion or sim.recuperados[-1] == sim.poblacion: 
            game_over = True

        # Actualizacion de pantalla #
        pygame.display.update() 
        FPSCLOCK.tick(FPS) 

# Llamado a función principal #
if __name__ == '__main__':
    main()
