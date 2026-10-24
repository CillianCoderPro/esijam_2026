import pygame

# ------------------------------ Pygame ----------------------------------
INITIAL_SCREEN_SIZE = (600,600)
CAPTION = "esijam_2026"
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode(INITIAL_SCREEN_SIZE, pygame.RESIZABLE)

# -------------------------------- CONROLS -------------------------------------------

MOVES = {
    pygame.K_z: (-1, 0, 0),
    pygame.K_s: (1, 0, 0),
    pygame.K_q: (0, -1, 0),
    pygame.K_d: (0, 1, 0),
    pygame.K_SPACE: (0, 0, 1),
    pygame.K_LALT: (0, 0, -1)
}

#----------------------------------- World -------------------------------------------------

CUBE_SIZE = 40
NUMBER_OF_CUBES = 8
NUMBER_OF_LAYERS = 4
GAP_SIZE = 7# must be greater than 0
TOP_LAYER = NUMBER_OF_LAYERS - 1
TOTAL_GRID_HEIGHT = CUBE_SIZE * NUMBER_OF_CUBES * 0.5 - (NUMBER_OF_LAYERS - 1) * GAP_SIZE * CUBE_SIZE * 0.5


#--------------------------------------- SPRITES --------------------------------------------

WHITE_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/white_cube.png'), (CUBE_SIZE, CUBE_SIZE))
RED_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/red_cube.png'), (CUBE_SIZE, CUBE_SIZE))
BLUE_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/blue_cube.png'), (CUBE_SIZE, CUBE_SIZE))





