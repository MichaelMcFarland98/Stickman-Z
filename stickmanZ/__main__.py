
from game.game_view import GameView
from game.menu_view import menu_view
from game import constants
import arcade


SCREEN_WIDTH = constants.SCREEN_WIDTH
SCREEN_HEIGHT = constants.SCREEN_HEIGHT
SCREEN_TITLE = constants.SCREEN_TITLE

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
start_view = menu_view()
window.show_view(start_view)
arcade.run()

