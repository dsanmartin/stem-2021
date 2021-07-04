import sys
import pygame
from pygame.locals import *
from simulacion import Simulacion

# Colores utilizados en el juego #
NEGRO    = (0, 0, 0)
BLANCO   = (255, 255, 255)
AMARILLO = (255, 255, 102)
ROJO     = (255, 0, 0)
VERDE    = (0, 255, 0)
AZUL     = (0, 0, 255)
NARANJO  = (255, 165, 0)
CYAN     = (0, 255, 255)

# Colores para estados de personas #
COLORES = [VERDE, ROJO, AZUL]

# Pixeles pasto
PIX = 42

# Tamaño ventana
ANCHOVENTANA  = 650
ALTURAVENTANA = 400

# Area de juego#
XMIN = 10
XMAX = PIX * 11 + XMIN
YMIN = 10
YMAX = PIX * 10 + YMIN
ANCHO = XMAX - XMIN
ALTO = YMAX - YMIN
 
# Frames por segundo #
FPS = 5

# Radio de círculo #
RADIO = 5

# Ancho cuadrados #
ANCHOCUADRADO = 10

# Figures #
VACIMG = pygame.image.load('img/vaccine.png') # Vacuna
PERIMG = pygame.image.load('img/person.png') # Personas
PASTO = pygame.image.load('img/grass.jpg')

def colorize(imagen, color):
    """ Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    image: Surface to create a colorized copy of
    color: RGB color to use (original alpha values are preserved)
    return New colorized Surface instance
    """
    imagen = imagen.copy()

    # zero out RGB values
    imagen.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    imagen.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

    return imagen

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

def pos(x, y):
    """Coordenadas de plano cartesiano a coordenadas de pygame.

    Parámetros
    ----------
    posicion : tupla (int, int)
        Coordenadas en plano cartesiano.

    Retorna
    -------
    tuple
        Retorna la posición en coordenadas de pygame
    """
    return (XMIN + x, YMAX - y)

def dibujar_vacuna(display, posicion):
    #pygame.draw.rect(display, NARANJO, pygame.Rect(posicion[0], posicion[1], ANCHOCUADRADO, ANCHOCUADRADO))
    # color_surface(VACCOL, 255, 0, 0)
    display.blit(VACIMG, posicion)

def dibujar_persona(display, posicion, color):
    #pygame.draw.circle(display, color, posicion, RADIO)
    display.blit(colorize(PERIMG, color), posicion)

def dibujar_pasto(display):
    fil = ALTO // PIX
    col = ANCHO // PIX
    # #pasto = PASTO.convert()
    # #pasto = pasto.set_alpha(128)
    # pasto = PASTO.copy()
    # # this works on images with per pixel alpha too
    # alpha = 250
    # pasto.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
    posy = 0
    for i in range(fil):
        posx = 0
        for j in range(col):
            display.blit(PASTO, (posx + XMIN, posy + YMIN))
            posx += PIX
        posy += PIX



def plot(display, personas, vacunas):
    # Dibujar personas
    for persona in personas:
        if persona.inoculacion > 0 and persona.estado != 1:
            dibujar_persona(display, pos(persona.x, persona.y), CYAN)
        else:
            dibujar_persona(display, pos(persona.x, persona.y), COLORES[persona.estado])
    # Dibujar vacunas
    for vacuna in vacunas:
        dibujar_vacuna(display, pos(vacuna.x, vacuna.y))

def counter(display, sim):
    font_1 = pygame.font.SysFont("Arial", 11, bold=True)
    font_2 = pygame.font.SysFont("Arial", 12)
    # Marco
    pygame.draw.rect(display, NEGRO, pygame.Rect(XMAX + 25, YMIN , 120, 100), width=1)
    # Titulo
    titulo = font_1.render("CONTADOR", 1, NEGRO)
    display.blit(titulo, (XMAX + 27, YMIN))
    # Etiquetas personas
    # Colores
    pygame.draw.circle(display, VERDE, (XMAX + 35, YMIN + 22), RADIO) # Sano
    pygame.draw.circle(display, ROJO, (XMAX + 35, YMIN + 42), RADIO) # Infectado
    pygame.draw.circle(display, AZUL, (XMAX + 35, YMIN + 62), RADIO) # Recuperado
    pygame.draw.circle(display, CYAN, (XMAX + 35, YMIN + 82), RADIO) # Vacunado
    #
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


def main():
    global FPSCLOCK, DISPLAY, BASICFONT
    game_over = False

    # Configuración PyGame #
    pygame.init() 
    FPSCLOCK = pygame.time.Clock() # Reloj del juego
    DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) # Tamaño de ventana
    BASICFONT = pygame.font.Font('freesansbold.ttf', 16) # Tipografía
    pygame.display.set_caption('Videojuégatela por la Inmunidad - STEM 2021') # Título de la ventana

    # Personas en la simulacion
    # El algoritmo de colisiones depende de la cantidad de personas. 
    # No debería utilizar más de 100, lo ideal es un valor menor.
    poblacion = 100
    # Vacunas disponible en el juego
    vacunas = 1
    # Dias de simulacion
    dias_simulacion = 100
    # Tamaño del "mundo"
    x_min = 0
    x_max = ANCHO
    y_min = 0
    y_max = ALTO
    # Porcentaje inicial de infectados
    porcentaje_infectados = 0.5
    # Probabilidad de que una persona se vacune
    probabilidad_vacuna = 1
    # Velocidad de movimiento personas (pixeles / tick)
    vel_per = 5
    # Velocidad de movimiento vacunas (pixeles / tick)
    vel_vac = 5
    # Objeto de simulación
    sim = Simulacion(poblacion, vacunas, dias_simulacion, x_min, x_max, y_min, y_max, 
        porc_infectados=porcentaje_infectados, prob_vacuna=probabilidad_vacuna)
    # Dia de simulacion
    d = 0 
    # Posicion inicial vacuna 
    sim.vacunas[0].x = x_max // 2
    sim.vacunas[0].y = y_max // 2

    # Loop principal del juego
    while not game_over:

        # Pantalla blanca
        DISPLAY.fill(BLANCO)

        # Dibujar el fondo con pasto
        dibujar_pasto(DISPLAY)

        # Marco
        #pygame.draw.rect(DISPLAY, NEGRO, pygame.Rect(XMIN, YMIN, XMAX, YMAX), width=2)

        # Contador estadísticas
        counter(DISPLAY, sim)

        # Revisar si se cierra el juego #
        revisar_final()

        # Consultar eventos de pygame (clic o teclas) #
        for event in pygame.event.get():
            # Mover vacuna utilizando el mouse
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                sim.vacunas[0].x, sim.vacunas[0].y = (mousex - XMIN, YMAX - mousey)
            # Mover vacuna utilizando el teclado
            elif event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    sim.vacunas[0].x -= vel_vac
                    sim.vacunas[0].x %= sim.x_max
                elif event.key == pygame.K_RIGHT:
                    sim.vacunas[0].x += vel_vac
                    sim.vacunas[0].x %= sim.x_max
                elif event.key == pygame.K_UP:
                    sim.vacunas[0].y += vel_vac
                    sim.vacunas[0].y %= sim.y_max
                elif event.key == pygame.K_DOWN:
                    sim.vacunas[0].y -= vel_vac
                    sim.vacunas[0].y %= sim.y_max

        # Etapas de simulacion #
        sim.mover_personas(vel_per) # Movimiento aleatorio de personas
        # Esperar por la revisión de colisiones
        # flag = True
        # while flag:
        #     if sim.mover_personas(vel_per):
        #         flag = False
        sim.revisar_contagio() # Simular el contagio
        #sim.mover_vacunas() # Mover las vacunas
        sim.revisar_vacunacion() # Simular el proceso de vacunación
        sim.estadisticas() # Obtención de estadísticas
        plot(DISPLAY, sim.personas, sim.vacunas) # Dibujar a los agentes
        d += 1 # Siguiente dia de simulación

        # Detener la simulación cuando se alcancel los días definidos o ya estén todos recuperados
        if d == sim.dias_simulacion or sim.recuperados[-1] == sim.poblacion: 
            game_over = True

        # Actualizacion de pantalla #
        pygame.display.update() 
        FPSCLOCK.tick(FPS) 

# Función principal #
if __name__ == '__main__':
    main()
