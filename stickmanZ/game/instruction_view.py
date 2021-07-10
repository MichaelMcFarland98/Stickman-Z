import arcade
from game.game_view import GameView
from game import constants


class InstructionView(arcade.View):
    
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("How to Play", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Use W, A, S, D to move around.", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-25,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Use the mouse to aim and the left mouse button to shoot.", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")                 
        arcade.draw_text("Good luck! Click to advance", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-80,
                         arcade.color.GRAY, font_size=15, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        start_game = GameView()
        self.window.show_view(start_game)