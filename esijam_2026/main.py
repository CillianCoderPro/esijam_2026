from Scene import *


menu = MenuScene()
game = GameScene()
return_to_manu = BackToMenu()
state_machine = StateMachine({"menu": menu, "game": game, "back_to_menu": return_to_manu}, "menu")
state_machine.run()


"""
TO DO:

- Fix UI: upgrade buttons
- Falling animation for players
- Enemy AI
- Sounds

"""

