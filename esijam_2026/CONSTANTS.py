import pygame
from Button import Button

# ------------------------------ Pygame ----------------------------------
pygame.init()

INITIAL_SCREEN_SIZE = (600,600)
CAPTION = " 'Esi'metric Spleef"
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode(INITIAL_SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption(CAPTION)

#----------------------------------- World -------------------------------------------------

CUBE_SIZE = 35
NUMBER_OF_CUBES = 13
NUMBER_OF_LAYERS = 3
GAP_SIZE = 15# must be greater than 0
TOP_LAYER = NUMBER_OF_LAYERS - 1
TOTAL_GRID_HEIGHT = CUBE_SIZE * NUMBER_OF_CUBES * 0.5 - (NUMBER_OF_LAYERS - 1) * GAP_SIZE * CUBE_SIZE * 0.5

FRAMES_BEFORE_CUBE_BREAKS = 24

GRAVITY = 1 #pixels fallen per frame


BACKROUND_COLOUR = (100, 150, 100)


#--------------------------------------- SPRITES --------------------------------------------

WHITE_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/white_cube.png'), (CUBE_SIZE, CUBE_SIZE))
RED_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/red_cube.png'), (CUBE_SIZE, CUBE_SIZE))
BLUE_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/blue_cube.png'), (CUBE_SIZE, CUBE_SIZE))
YELLOW_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/yellow_cube.png'), (CUBE_SIZE, CUBE_SIZE))
GREEN_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/green_cube.png'), (CUBE_SIZE, CUBE_SIZE))
BLACK_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/black_cube.png'), (CUBE_SIZE, CUBE_SIZE))
BROKEN_1_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/broken_cube_1.png'), (CUBE_SIZE, CUBE_SIZE))
BROKEN_2_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/broken_cube_2.png'), (CUBE_SIZE, CUBE_SIZE))
BROKEN_3_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/broken_cube_3.png'), (CUBE_SIZE, CUBE_SIZE))
BLANK_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/blank_cube.png'), (CUBE_SIZE, CUBE_SIZE))
FULL_WHITE_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/full_white_cube.png'), (CUBE_SIZE, CUBE_SIZE))


GRID_CUBE_IMAGES = (
    WHITE_CUBE_IMAGE,
    BROKEN_1_CUBE_IMAGE,
    BROKEN_2_CUBE_IMAGE,
    BROKEN_3_CUBE_IMAGE,
    BLANK_CUBE_IMAGE,
)
NUMBER_OF_GRID_CUBE_IMAGES = len(GRID_CUBE_IMAGES)

# -------------------------------- PLAYER SETTINGS -------------------------------------------

PLAYER_CONFIGURATIONS = (
    {   "start": (0,0),
        "image": RED_CUBE_IMAGE,
        "name": "Red Cube",
        "moves":{
                pygame.K_z: (-1, 0, 0),
                pygame.K_s: (1, 0, 0),
                pygame.K_q: (0, -1, 0),
                pygame.K_d: (0, 1, 0),
                }
    },

    {   "start": (NUMBER_OF_CUBES-1,NUMBER_OF_CUBES-1),
        "image": BLUE_CUBE_IMAGE,
        "name": "Blue Cube",
        "moves":{
                pygame.K_UP: (-1, 0, 0),
                pygame.K_DOWN: (1, 0, 0),
                pygame.K_LEFT: (0, -1, 0),
                pygame.K_RIGHT: (0, 1, 0),
                }
    },

    {   "start": (0,NUMBER_OF_CUBES-1),
        "image": YELLOW_CUBE_IMAGE,
        "name": "Yellow Cube",
        "moves":{
                pygame.K_i: (-1, 0, 0),
                pygame.K_k: (1, 0, 0),
                pygame.K_j: (0, -1, 0),
                pygame.K_l: (0, 1, 0),
                }
    },

    {   "start": (NUMBER_OF_CUBES-1, 0),
        "image": GREEN_CUBE_IMAGE,
        "name": "Green Cube",
        "moves":{
                pygame.K_t: (-1, 0, 0),
                pygame.K_g: (1, 0, 0),
                pygame.K_f: (0, -1, 0),
                pygame.K_h: (0, 1, 0),
                }
    },
)

NUMBER_OF_PLAYERS = 4

VALID_BOT_MOVES = ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1))




# -------------------------------- BOT SETTINGS -------------------------------------------


BOT_MOVE_INTERVAL = 20 #frames between bot decisions (60 frames = 1 second)




# -------------------------------- SOUND -------------------------------------------



pygame.mixer.init()
BREAK_SOUND = pygame.mixer.Sound("sounds/break.mp3")
BREAK_SOUND.set_volume(1)
POP_SOUND = pygame.mixer.Sound("sounds/pop.mp3")
BACKROUND_MUSIC = pygame.mixer.Sound("sounds/music1.mp3")
BACKROUND_MUSIC.set_volume(0.1)



# ------------------------------------ FONTS + TEXT + BUTTONS ---------------------------------

#FONT = pygame.font.Font(None, 20)
FONT_PATH = "PressStart2P-Regular.ttf"
FONT_SIZE = 24
FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)


# Home Screen Buttons:

BUTTON_AI = Button(0,-250, 300, 60, SCREEN, FONT, "Play vs AI")
BUTTON1 = Button(0,-150, 300, 60, SCREEN, FONT,"2 players")
BUTTON2 = Button(0,-50, 300, 60, SCREEN, FONT,"3 players")
BUTTON3 = Button(0,50, 300, 60, SCREEN, FONT,"4 players")
BUTTON4 = Button(0,150, 300, 60, SCREEN, FONT,"Quit")