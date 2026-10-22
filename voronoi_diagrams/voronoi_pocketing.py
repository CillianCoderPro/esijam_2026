import pygame
from random import randint
from math import sqrt

pygame.init()

screen = pygame.display.set_mode((750,750))
screen_width, screen_height = screen.get_size()

class Point:
    def __init__(self, X, Y, VORONOI_COL,point_col = "RED",point_radius = 1):
        self.x = X
        self.y = Y
        self.voronoi_col = VORONOI_COL
        self.point_col = point_col
        self.point_radius = point_radius

    def distance(self,x,y):
        return sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def draw(self):
        pygame.draw.circle(screen,self.point_col,(self.x,self.y),self.point_radius)

class Diagrams:
    def __init__(self,PLATE_WIDTH, PLATE_HEIGHT, LIST = []):
        self.left_side = screen_width // 2 - PLATE_WIDTH // 2
        self.right_side = screen_width // 2 + PLATE_WIDTH // 2
        self.top_side = screen_height // 2 - PLATE_HEIGHT // 2
        self.bottom_side = screen_height // 2 + PLATE_HEIGHT // 2
        self.plate_width = PLATE_WIDTH
        self.plate_height = PLATE_HEIGHT
        self.point_list = LIST
        print(self.left_side, self.right_side, self.top_side, self.bottom_side)

    def create_points(self, number_of_points):
        self.point_list = []
        for _ in range(number_of_points):
            x = randint(self.left_side,self.right_side)
            y = randint(self.top_side,self.bottom_side)
            #col = (randint(0,255),randint(0,255),randint(0,255))
            col = "WHITE"
            point = Point(x, y, col)
            self.point_list.append(point)

    def get_closest_point(self, x, y):
        return min(self.point_list, key=lambda p: p.distance(x, y))

    def draw(self):
        # First pass: compute the closest point for every pixel
        ownership = {}
        for x in range(self.left_side, self.right_side):
            for y in range(self.top_side, self.bottom_side):
                ownership[(x, y)] = self.get_closest_point(x, y)

        border_thickness = 4  # adjust as needed

        # Second pass: color pixels
        for x in range(self.left_side, self.right_side):
            for y in range(self.top_side, self.bottom_side):
                owner = ownership[(x, y)]

                # Check all neighbors within border_thickness
                is_border = False
                for dx in range(-border_thickness, border_thickness + 1):
                    for dy in range(-border_thickness, border_thickness + 1):
                        neighbor = ownership.get((x + dx, y + dy))
                        if neighbor is not None and neighbor is not owner:
                            is_border = True
                            break
                    if is_border:
                        break

                col = "BLACK" if is_border else owner.voronoi_col
                pygame.draw.rect(screen, col, pygame.Rect(x, y, 1, 1))

        for point in self.point_list:
            point.draw()

plate_width, plate_height = 600, 200
diagrams = Diagrams(plate_width, plate_height)
diagrams.create_points(10)
diagrams.draw()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("space pressed")

    pygame.display.flip()
