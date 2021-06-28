import pygame
from pygame.locals import *
import time
import random
import sys
from simulacion import Simulacion

# Game colors #
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
YELLOW = (255, 255, 102)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
ORANGE = (255, 165, 0)
CYAN   = (0, 255, 255)

# Colores para estados de personas #
COLORES = [GREEN, RED, BLUE]

# Display size
WINDOWWIDTH  = 650
WINDOWHEIGHT = 400

# Playable area #
XMIN, XMAX = 10, 500
YMIN, YMAX = 10, 380
 
# Frames per seconds #
FPS = 5

# Circle radius #
RADIUS = 5

# Square width #
SQUAREWIDTH = 10

# Movement #
MOV = 5

# def message(msg, color):
#     mesg = font_style.render(msg, True, color)
#     dis.blit(mesg, [WIDTH / 6, HEIGHT / 3])

def terminar():
    pygame.quit()
    sys.exit()

def revisar_final():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminar() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminar() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def pos(posicion):
    """Plano cartesiano a coordenadas de pygame.

    Parámetros
    ----------
    posicion : tupla (int, int)
        Coordenadas en plano cartesiano.

    Retorna
    -------
    tuple
        Retorna la posición en coordenadas de pygame
    """
    return (XMIN + posicion[0], YMAX - posicion[1])

def dibujar_vacuna(display, posicion):
    pygame.draw.rect(display, ORANGE, pygame.Rect(posicion[0], posicion[1], SQUAREWIDTH, SQUAREWIDTH))

def dibujar_persona(display, posicion, color):
    pygame.draw.circle(display, color, posicion, RADIUS)

def plot(display, personas, vacunas):
    # Dibujar personas
    for persona in personas:
        if persona.inoculacion > 0 and persona.estado != 1:
            dibujar_persona(display, pos((persona.x, persona.y)), CYAN)
        else:
            dibujar_persona(display, pos((persona.x, persona.y)), COLORES[persona.estado])
    # Dibujar vacunas
    for vacuna in vacunas:
        dibujar_vacuna(display, pos((vacuna.x, vacuna.y)))

def counter(display, sim):
    font_1 = pygame.font.SysFont("Arial", 11, bold=True)
    font_2 = pygame.font.SysFont("Arial", 12)
    # Marco
    pygame.draw.rect(display, BLACK, pygame.Rect(XMAX + 25, YMIN , 120, 100), width=1)
    # Titulo
    titulo = font_1.render("CONTADOR", 1, BLACK)
    display.blit(titulo, (XMAX + 27, YMIN))
    # Etiquetas personas
    # Colores
    pygame.draw.circle(display, GREEN, (XMAX + 35, YMIN + 22), RADIUS) # Sano
    pygame.draw.circle(display, RED, (XMAX + 35, YMIN + 42), RADIUS) # Infectado
    pygame.draw.circle(display, BLUE, (XMAX + 35, YMIN + 62), RADIUS) # Recuperado
    pygame.draw.circle(display, CYAN, (XMAX + 35, YMIN + 82), RADIUS) # Vacunado
    #
    n_sanos = sim.sanos[-1] if len(sim.sanos) > 0 else 0
    n_infec = sim.infectados[-1] if len(sim.infectados) > 0 else 0
    n_recup = sim.recuperados[-1] if len(sim.recuperados) > 0 else 0
    n_vacun = sim.inoculados[-1] if len(sim.inoculados) > 0 else 0

    # Texto
    label = font_2.render("Sanos " + str(n_sanos), 1, BLACK)
    display.blit(label, (XMAX + 42, YMIN + 16))
    label = font_2.render("Infectados " + str(n_infec), 1, BLACK)
    display.blit(label, (XMAX + 42, YMIN + 36))
    label = font_2.render("Recuperados " + str(n_recup), 1, BLACK)
    display.blit(label, (XMAX + 42, YMIN + 56))
    label = font_2.render("Vacunados " + str(n_vacun), 1, BLACK)
    display.blit(label, (XMAX + 42, YMIN + 76))


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    game_over = False

    # Configuración PyGame #
    pygame.init() 
    FPSCLOCK = pygame.time.Clock() # Reloj del juego
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) # Tamaño de ventana
    pygame.display.set_caption('Videojuégatela por la Inmunidad - STEM 2021') # Título de la ventana
    BASICFONT = pygame.font.Font('freesansbold.ttf', 16) # Tipografía

    # Personas en la simulacion
    poblacion = 100
    # Vacunas disponible en el juego
    vacunas = 1
    # Dias de simulacion
    dias_simulacion = 300
    # Tamaño del "mundo"
    x_min = 0
    x_max = XMAX - XMIN
    y_min = 0
    y_max = YMAX - YMIN
    # Porcentaje inicial de infectados
    porcentaje_infectados = 0.5
    # Objeto de simulación
    sim = Simulacion(poblacion, vacunas, dias_simulacion, x_min, x_max, y_min, y_max, 
        porc_infectados=porcentaje_infectados)
    d = 0 # Dia de simulacion
    # Posicion inicial vacuna 
    sim.vacunas[0].x = x_max // 2
    sim.vacunas[0].y = y_max // 2

    # Loop principal del juego
    while not game_over:

        # Pantalla blanca
        DISPLAYSURF.fill(WHITE)

        # Marco
        pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect(XMIN, YMIN, XMAX, YMAX), width=2)

        # Contador estadísticas
        counter(DISPLAYSURF, sim)

        # Revisar si se cierra el juego #
        revisar_final()

        # Consultar eventos de pygame (clic o teclas) #
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                print(mousex, mousey)
                #clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    sim.vacunas[0].x -= MOV
                    sim.vacunas[0].x %= sim.x_max
                elif event.key == pygame.K_RIGHT:
                    sim.vacunas[0].x += MOV
                    sim.vacunas[0].x %= sim.x_max
                elif event.key == pygame.K_UP:
                    sim.vacunas[0].y += MOV
                    sim.vacunas[0].y %= sim.y_max
                elif event.key == pygame.K_DOWN:
                    sim.vacunas[0].y -= MOV
                    sim.vacunas[0].y %= sim.y_max

        # Etapas de simulacion #
        sim.mover_personas() # Movimiento aleatorio de personas
        sim.revisar_contagio() # Simular el contagio
        #sim.mover_vacunas() # Mover las vacunas
        sim.revisar_vacunacion() # Simular el proceso de vacunación
        sim.estadisticas() # Obtención de estadísticas
        plot(DISPLAYSURF, sim.personas, sim.vacunas) # Dibujar a los agentes
        d += 1 # Siguiente dia de simulación
        # Detener la simulación cuando se alcancel los días definidos o ya estén todos recuperados
        if d == sim.dias_simulacion or sim.recuperados[-1] == sim.poblacion: 
            game_over = True
        
        # Actualizacion de pantalla #
        pygame.display.update() # Actualización de pantalla
        FPSCLOCK.tick(FPS) 

# Función principal #
if __name__ == '__main__':
    main()
