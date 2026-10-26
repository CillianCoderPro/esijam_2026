import pygame


class Button:

    def __init__(self, x, y, width, height, screen, text = "button", colour = (200, 100, 100)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.font = pygame.font.Font(None, 20)
        self.text = self.font.render(text, True, (0,0,0))
        self.colour = colour

    def screen_x(self):
        x_offset = self.screen.get_width() / 2 - self.width/2
        screen_x = self.x + x_offset
        return screen_x

    def screen_y(self):
        y_offset = (self.screen.get_height()) / 2 - self.height/2
        screen_y = self.y + y_offset
        return screen_y

    def mouse_hover(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (self.screen_x() < mouse_x and mouse_x < self.screen_x() + self.width) and (self.screen_y() < mouse_y and mouse_y < self.screen_y() + self.height)

    def clicked(self, event):
        if not self.mouse_hover():
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True

    def draw(self):
        button_square = pygame.Surface((self.width, self.height))
        if self.mouse_hover():
            button_square.fill((50,50,200))
        else:
            button_square.fill((self.colour))
        self.screen.blit(button_square, (self.screen_x(), self.screen_y()))
        self.screen.blit(self.text, (self.screen_x(), self.screen_y()))


