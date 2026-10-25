import pygame

from CONSTANTS import *


class Scene:
    def __init__(self):
        self.next_state = None
        self.next_data = {}

    def on_enter(self, data): pass
    def handle_event(self, event): pass
    def update(self): pass
    def draw(self, screen): pass

class StateMachine():
    def __init__(self, scene_dict, start_name):
        self.current_scene = scene_dict[start_name]
        self.scene_dict = scene_dict
        self.current_scene.on_enter({})

    def change(self, name, data):
        self.current_scene = self.scene_dict[name]
        self.current_scene.next_state = None
        self.current_scene.on_enter(data)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.current_scene.handle_event(event)

            self.current_scene.update()
            if self.current_scene.next_state == "quit":
                pygame.quit()
                exit()
            elif self.current_scene.next_state:
                self.change(self.current_scene.next_state, self.current_scene.next_data)

            self.current_scene.draw(SCREEN)
            pygame.display.flip()
            CLOCK.tick(60)

class MenuScene(Scene):
    def __init__(self):
        super().__init__()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "quit"
    def draw(self, screen):
        screen.fill((200,100,100))
        screen.blit(TEXT, (screen.get_width()//2, screen.get_height()//2))

class GameScene(Scene):
    def __init__(self, number_of_players, list_of_players, grid):
        super().__init__()
        self.number_of_players = number_of_players
        self.list_of_players = list_of_players
        self.grid = grid

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "quit"
            for i, player in enumerate(self.list_of_players):
                if event.key in PLAYER_CONFIGURATIONS[i]["moves"]:
                    d_row,d_file,d_col = PLAYER_CONFIGURATIONS[i]["moves"][event.key]
                    player.move(d_row, d_file, d_col, self.grid, self.list_of_players)

    def update(self):
        for player in self.list_of_players:
            player.update_state(self.grid)

    def draw(self, screen):
        SCREEN.fill((100, 150, 100))
        grid.draw(list_of_players)




from Cube import Player
from Grid import Grid

grid = Grid()
list_of_players = []

for i in range(NUMBER_OF_PLAYERS):
    row, file = PLAYER_CONFIGURATIONS[i]["start"]
    image = PLAYER_CONFIGURATIONS[i]["image"]
    player = Player(row, file, TOP_LAYER, image)
    list_of_players.append(player)


menu = MenuScene()
game = GameScene(NUMBER_OF_CUBES, list_of_players, grid)
state_machine = StateMachine({"menu": menu, "game": game}, "game")
state_machine.run()

from Cube import Player
from Grid import Grid
