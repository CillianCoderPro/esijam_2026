from Scene import *


menu = MenuScene()
game = GameScene()
back_to_menu = BackToMenu()
state_machine = StateMachine({"menu": menu, "game": game, "back_to_menu": back_to_menu}, "menu")
state_machine.run()


"""
TO DO:

- Fix UI: upgrade buttons
- Enemy AI
- Sounds

"""

