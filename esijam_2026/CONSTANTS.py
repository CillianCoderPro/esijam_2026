import pygame

""" pygame stuff"""
INITIAL_SCREEN_SIZE = (600,600)
CAPTION = "esijam_2026"
CLOCK = pygame.time.Clock()

"""sprites"""
CUBE_SIZE = 50
WHITE_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/white_cube.png'), (CUBE_SIZE, CUBE_SIZE))
RED_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/red_cube.png'), (CUBE_SIZE, CUBE_SIZE))
BLUE_CUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/blue_cube.png'), (CUBE_SIZE, CUBE_SIZE))





