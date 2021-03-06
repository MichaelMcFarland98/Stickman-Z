import arcade
from game import constants
# from game.menu_view import menu_view

class GameOverView(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.score = score
        

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """
        Draw Death Notice across the screen and give player total score
    
        """
        
        HEIGHT = constants.SCREEN_HEIGHT
        WIDTH = constants.SCREEN_WIDTH
        TITLE = constants.SCREEN_TITLE
        arcade.start_render()
        
        arcade.draw_text("You Died...", constants.SCREEN_HEIGHT / 2, constants.SCREEN_WIDTH / 2, arcade.color.WHITE, 54)

        if self.score <= 500:
            arcade.draw_text("I rather fight zombies by myself than with you...", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-25, arcade.color.WHITE, font_size=20, anchor_x="center")
        elif self.score <= 1000 and self.score > 500:
            arcade.draw_text("You got an okay shot, maybe try not dying next time.", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-25, arcade.color.WHITE, font_size=20, anchor_x="center")
        elif self.score > 1000:
            arcade.draw_text("Are you related to John Wick, or maybe Chuck Norris??", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-25, arcade.color.WHITE, font_size=20, anchor_x="center")
        else:
            arcade.draw_text("Something isn't right...", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-25, arcade.color.WHITE, font_size=20, anchor_x="center")



        time_taken_formatted = f"{round(self.score, 2)} points"
        arcade.draw_text(f"Your Score: {time_taken_formatted}",
                         WIDTH/2,
                         200,
                         arcade.color.GRAY,
                         font_size=15,
                         anchor_x="center")


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # start_view = menu_view()
        # self.window.show_view(start_view)
        pass

