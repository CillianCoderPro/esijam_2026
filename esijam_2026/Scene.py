from CONSTANTS import *
from Cube import Player
from Grid import Grid

### -------------------------------------- Parent Scene Class ------------------------------------------



class Scene:
    def __init__(self):
        self.next_state = None
        self.next_data = {}

    def on_enter(self, data): pass
    def handle_event(self, event): pass
    def update(self): pass
    def draw(self, screen): pass


### -------------------------------------- State Machine ------------------------------------------




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

### --------------------------------------  Menu Screen ------------------------------------------



class MenuScene(Scene):
    def __init__(self):
        super().__init__()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "quit"
        if BUTTON_AI.clicked(event):
            self.next_state = "game"
            self.next_data = {"number_of_players":1, "number_of_bots": 3}
        if BUTTON1.clicked(event):
            self.next_state = "game"
            self.next_data = {"number_of_players":2, "number_of_bots": 0}
        if BUTTON2.clicked(event):
            self.next_state = "game"
            self.next_data = {"number_of_players":3, "number_of_bots": 0}
        if BUTTON3.clicked(event):
            self.next_state = "game"
            self.next_data = {"number_of_players":4, "number_of_bots": 0}
        if BUTTON4.clicked(event):
            self.next_state = "quit"

    def draw(self, screen):
        screen.fill((100,200,100))
        BUTTON_AI.draw()
        BUTTON1.draw()
        BUTTON2.draw()
        BUTTON3.draw()
        BUTTON4.draw()



### -------------------------------------- Main Game Screen ------------------------------------------




class GameScene(Scene):
    def __init__(self):
        super().__init__()

    def on_enter(self, data):
        self.number_of_players = data["number_of_players"]
        self.number_of_bots = data["number_of_bots"]
        self.list_of_players = []
        self.list_of_bots = []
        self.grid = Grid()
        self.frame = 0
        for i in range(self.number_of_players):
            row, file = PLAYER_CONFIGURATIONS[i]["start"]
            image = PLAYER_CONFIGURATIONS[i]["image"]
            name = PLAYER_CONFIGURATIONS[i]["name"]
            player = Player(row, file, TOP_LAYER, image, name)
            self.list_of_players.append(player)
        for i in range(self.number_of_players, self.number_of_bots+self.number_of_players):
            row, file = PLAYER_CONFIGURATIONS[i]["start"]
            image = PLAYER_CONFIGURATIONS[i]["image"]
            name = PLAYER_CONFIGURATIONS[i]["name"]
            bot = Player(row, file, TOP_LAYER, image, name)
            self.list_of_bots.append(bot)

    def all_players(self):
        return self.list_of_players + self.list_of_bots

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "quit"
            for i, player in enumerate(self.list_of_players):
                if event.key in PLAYER_CONFIGURATIONS[i]["moves"]:
                    d_row,d_file,d_col = PLAYER_CONFIGURATIONS[i]["moves"][event.key]
                    player.move(d_row, d_file, d_col, self.grid, self.all_players())

    def update(self):
        for player in self.all_players():
            player.update_state(self.grid)
        self.frame +=1
        if self.frame % BOT_MOVE_INTERVAL == 0: # delay between bot decisions
            for bot in self.list_of_bots:
                bot.bot_turn(self.grid, self.all_players())
        list_of_alive_players = [player for player in self.all_players() if player.state != "eliminated"]
        if len(list_of_alive_players) == 1:
            print(f"{list_of_alive_players[0].player_name} wins")
            self.next_state = "back_to_menu"
            self.next_data = {"winner": list_of_alive_players[0].player_name}

    def draw(self, screen):
        SCREEN.fill((100, 150, 100))
        self.grid.draw(self.all_players())




### -------------------------------------- Back To Menu Screen ------------------------------------------


class BackToMenu(Scene):
    def __init__(self):
        super().__init__()
        self.back_home_button = Button(0, 0, 200, 120, SCREEN, "Back to Home")

    def on_enter(self, data):
        self.winner = data["winner"]
        self.back_home_button = Button(0, 0, 200, 120, SCREEN, f"{self.winner} wins - Back To Home")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "quit"
        if self.back_home_button.clicked(event):
            self.next_state = "menu"

    def draw(self, screen):
        self.back_home_button.draw()

