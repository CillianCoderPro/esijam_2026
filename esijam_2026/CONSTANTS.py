import pygame


# ------------------------------ Pygame ----------------------------------
pygame.init()

INITIAL_SCREEN_SIZE = (600,600)
CAPTION = "esijam_2026"
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode(INITIAL_SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption(CAPTION)

#----------------------------------- World -------------------------------------------------

CUBE_SIZE = 50
NUMBER_OF_CUBES = 9
NUMBER_OF_LAYERS = 3
GAP_SIZE = 7# must be greater than 0
TOP_LAYER = NUMBER_OF_LAYERS - 1
TOTAL_GRID_HEIGHT = CUBE_SIZE * NUMBER_OF_CUBES * 0.5 - (NUMBER_OF_LAYERS - 1) * GAP_SIZE * CUBE_SIZE * 0.5




#--------------------------------------- SPRITES --------------------------------------------

WHITE_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/white_cube.png'), (CUBE_SIZE, CUBE_SIZE))
RED_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/red_cube.png'), (CUBE_SIZE, CUBE_SIZE))
BLUE_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/blue_cube.png'), (CUBE_SIZE, CUBE_SIZE))
YELLOW_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/yellow_cube.png'), (CUBE_SIZE, CUBE_SIZE))
GREEN_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/green_cube.png'), (CUBE_SIZE, CUBE_SIZE))
BLACK_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/black_cube.png'), (CUBE_SIZE, CUBE_SIZE))

# -------------------------------- PLAYER SETTINGS -------------------------------------------

PLAYER_CONFIGURATIONS = (
    {   "start": (0,0),
        "image": RED_CUBE_IMAGE,
        "moves":{
                pygame.K_z: (-1, 0, 0),
                pygame.K_s: (1, 0, 0),
                pygame.K_q: (0, -1, 0),
                pygame.K_d: (0, 1, 0),
                }
    },

    {   "start": (NUMBER_OF_CUBES-1,NUMBER_OF_CUBES-1),
        "image": BLUE_CUBE_IMAGE,
        "moves":{
                pygame.K_UP: (-1, 0, 0),
                pygame.K_DOWN: (1, 0, 0),
                pygame.K_LEFT: (0, -1, 0),
                pygame.K_RIGHT: (0, 1, 0),
                }
    },

    {   "start": (0,NUMBER_OF_CUBES-1),
        "image": YELLOW_CUBE_IMAGE,
        "moves":{
                pygame.K_i: (-1, 0, 0),
                pygame.K_k: (1, 0, 0),
                pygame.K_j: (0, -1, 0),
                pygame.K_l: (0, 1, 0),
                }
    },

    {   "start": (NUMBER_OF_CUBES-1, 0),
        "image": GREEN_CUBE_IMAGE,
        "moves":{
                pygame.K_t: (-1, 0, 0),
                pygame.K_g: (1, 0, 0),
                pygame.K_f: (0, -1, 0),
                pygame.K_h: (0, 1, 0),
                }
    },
)

NUMBER_OF_PLAYERS = 4



