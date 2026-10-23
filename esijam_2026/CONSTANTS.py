import pygame

""" pygame stuff"""
INITIAL_SCREEN_SIZE = (600,600)
CAPTION = "esijam_2026"
CLOCK = pygame.time.Clock()

CUBE_SIZE = 50
NUMBER_OF_CUBES = 5
NUMBER_OF_LAYERS = 4
GAP_SIZE = 7# must be greater than 0
TOP_LAYER = NUMBER_OF_LAYERS - 1
TOTAL_GRID_HEIGHT = CUBE_SIZE * NUMBER_OF_CUBES * 0.5 - (NUMBER_OF_LAYERS - 1) * GAP_SIZE * CUBE_SIZE * 0.5

"""sprites"""
WHITE_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/white_cube.png'), (CUBE_SIZE, CUBE_SIZE))
RED_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/red_cube.png'), (CUBE_SIZE, CUBE_SIZE))
BLUE_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/blue_cube.png'), (CUBE_SIZE, CUBE_SIZE))





