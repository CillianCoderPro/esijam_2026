import pygame


class Button:

    def __init__(self, x, y, width, height, colour = (100, 200, 100)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

    def screen_x(self, screen):
        x_offset = screen.get_width() / 2 - self.width/2
        screen_x = self.x + x_offset
        return screen_x

    def screen_y(self, screen):
        y_offset = (screen.get_height()) / 2 - self.height/2
        screen_y = self.y + y_offset
        return screen_y

    def draw(self, screen):
        button_square = pygame.Surface((self.width, self.height))
        button_square.fill((self.colour))
        screen.blit(button_square, (self.screen_x(screen), self.screen_y(screen)))


pygame.init()

INITIAL_SCREEN_SIZE = (600,600)
CAPTION = "button test"
SCREEN = pygame.display.set_mode(INITIAL_SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption(CAPTION)

button1 = Button(0,0, 100, 60)
SCREEN.fill((0,0,0))
button1.draw(SCREEN)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

