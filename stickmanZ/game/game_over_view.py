import arcade
from game import constants

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

        time_taken_formatted = f"{round(self.score, 2)} points"
        arcade.draw_text(f"Your Score: {time_taken_formatted}",
                         WIDTH/2,
                         200,
                         arcade.color.GRAY,
                         font_size=15,
                         anchor_x="center")


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        pass
    #Add Play again on wish list  

