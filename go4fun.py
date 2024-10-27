import pygame
import numpy as np
from G4C.go4.go4 import *
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre (exemple pour un goban 9x9 avec une case de 50 pixels)
GRID_SIZE = 19  # nombre de lignes/colonnes
CELL_SIZE = 40  # taille d'une case en pixels
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Jeu de Go à 4 joueurs")

# Couleurs
BACKGROUND_COLOR = (238, 203, 173)  # couleur du goban
LINE_COLOR = (0, 0, 0)  # couleur des lignes de la grille
STONE_COLOR_BLACK = (0, 0, 0)
STONE_COLOR_RED = (250, 30, 50)
STONE_COLOR_BLUE = (30, 50, 250)
STONE_COLOR_WHITE = (245, 240, 230)
STONE_COLOR_BLACK_TRANSPARENT = (0, 0, 0, 128)  # pierre noire transparente pour le survol
STONE_COLOR_RED_TRANSPARENT = (250, 30, 50, 128)
STONE_COLOR_BLUE_TRANSPARENT = (30, 50, 250, 128)
STONE_COLOR_WHITE_TRANSPARENT = (245, 240, 230, 128)


game = Position()
print(game.to_play)

# Index entre couleur de la pierre transparente et couleur du joueur
color_trans_stone = {-2:STONE_COLOR_RED_TRANSPARENT,1:STONE_COLOR_BLACK_TRANSPARENT,2:STONE_COLOR_BLUE_TRANSPARENT,-1:STONE_COLOR_WHITE_TRANSPARENT}

# Boucle principale du jeu
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            grid_x = round(mouse_x / CELL_SIZE)
            grid_y = round(mouse_y / CELL_SIZE)

            
            try:
                #On propose au moteur de jouer le coup !
                game = game.play_move((grid_y-1,grid_x-1))
                print(game)
            
            except KoError as e:
                print("Erreur de ko :", e)
        
            except OccupiedSpaceError as e:
                print("Erreur d'espace occupé :", e)
        
            except NoLibertyError as e:
                print("Erreur de liberté :", e)
    
    
    # Afficher le fond
    screen.fill(BACKGROUND_COLOR)

    # Dessiner la grille du goban
    for i in range(GRID_SIZE):
        # Lignes horizontales
        pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE, (i + 1) * CELL_SIZE), (WINDOW_SIZE - CELL_SIZE, (i + 1) * CELL_SIZE), 2)
        # Lignes verticales
        pygame.draw.line(screen, LINE_COLOR, ((i + 1) * CELL_SIZE, CELL_SIZE), ((i + 1) * CELL_SIZE, WINDOW_SIZE - CELL_SIZE), 2)

    # definir la couleur des pierre et les dessiner !
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if game.board[y][x] == -2:
                stone_color = STONE_COLOR_RED
                pygame.draw.circle(screen, stone_color, ((x+1) * CELL_SIZE, (y+1) * CELL_SIZE), CELL_SIZE // 2.2)
            elif game.board[y][x] == -1:
                stone_color = STONE_COLOR_WHITE
                pygame.draw.circle(screen, stone_color, ((x+1) * CELL_SIZE, (y+1) * CELL_SIZE), CELL_SIZE // 2.2)
            elif game.board[y][x] == 1:
                stone_color = STONE_COLOR_BLACK
                pygame.draw.circle(screen, stone_color, ((x+1) * CELL_SIZE, (y+1) * CELL_SIZE), CELL_SIZE // 2.2)
            elif game.board[y][x] == 2:
                stone_color = STONE_COLOR_BLUE
                pygame.draw.circle(screen, stone_color, ((x+1) * CELL_SIZE, (y+1) * CELL_SIZE), CELL_SIZE // 2.2)


    # Récupérer la position de la souris
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculer l'intersection la plus proche de la souris
    closest_x = round(mouse_x / CELL_SIZE) * CELL_SIZE
    closest_y = round(mouse_y / CELL_SIZE) * CELL_SIZE

    # Afficher la pierre transparente en survol
    stone_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(stone_surface, color_trans_stone[game.to_play], (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 2.2)
    screen.blit(stone_surface, (closest_x - CELL_SIZE // 2, closest_y - CELL_SIZE // 2))

    # Rafraîchir l'écran
    pygame.display.flip()

# Quitter Pygame proprement
pygame.quit()
sys.exit()
