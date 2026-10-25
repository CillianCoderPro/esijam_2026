from CONSTANTS import *
from Cube import Player
from Grid import Grid

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
            elif event.key == pygame.K_2:
                self.next_state = "game"
                self.next_data = {"number_of_players":2}
            elif event.key == pygame.K_3:
                self.next_state = "game"
                self.next_data = {"number_of_players": 3}

    def draw(self, screen):
        screen.fill((200,100,100))
        screen.blit(TEXT, (screen.get_width()//2, screen.get_height()//2))

class GameScene(Scene):
    def __init__(self):
        super().__init__()

    def on_enter(self, data):
        self.number_of_players = data["number_of_players"]
        self.list_of_players = []
        self.grid = Grid()
        for i in range(self.number_of_players):
            row, file = PLAYER_CONFIGURATIONS[i]["start"]
            image = PLAYER_CONFIGURATIONS[i]["image"]
            player = Player(row, file, TOP_LAYER, image)
            self.list_of_players.append(player)

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
        self.grid.draw(self.list_of_players)






menu = MenuScene()
game = GameScene()
state_machine = StateMachine({"menu": menu, "game": game}, "menu")
state_machine.run()

