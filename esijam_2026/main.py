from Scene import *


menu = MenuScene()
game = GameScene()
return_to_manu = ReturnToMenu()
state_machine = StateMachine({"menu": menu, "game": game, "return_to_menu": return_to_manu}, "menu")
state_machine.run()


