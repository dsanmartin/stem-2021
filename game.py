import pygame
import time
import random

# Game colors #
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
YELLOW = (255, 255, 102)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)

# Display size
WIDTH  = 600
HEIGHT = 400
 
SPEED = 10

pygame.init()

# Define Display size
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Videojuégatela por la Inmunidad - STEM 2021') # Screen Title

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
 
clock = pygame.time.Clock()

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [WIDTH / 6, HEIGHT / 3])


def gameLoop():
    game_over = False
    game_close = False

    while not game_over:
        
        while not game_close:
            dis.fill(WHITE)
            message("You Lost! Press C-Play Again or Q-Quit", RED)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
        
        pygame.display.update()
        clock.tick(SPEED)

    pygame.quit()
    quit()

gameLoop()