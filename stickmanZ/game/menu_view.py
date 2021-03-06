import arcade
from game import constants
from game.game_view import GameView
from game.instruction_view import InstructionView

class menu_view(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.RED)

    def on_draw(self):
        WIDTH = constants.SCREEN_WIDTH
        HEIGHT = constants.SCREEN_HEIGHT
        TITLE = constants.SCREEN_TITLE

        arcade.start_render()
        arcade.draw_text(constants.SCREEN_TITLE, WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to play", WIDTH/2, HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instruction_view = InstructionView()
        self.window.show_view(instruction_view)