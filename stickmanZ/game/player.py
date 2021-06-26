from game import constants
import arcade
from game.point import Point

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(constants.PLAYER_IMAGE)

        self.center_x = int(constants.SCREEN_WIDTH / 2)
        self.center_y = int(constants.SCREEN_HEIGHT / 2)

        #Make sure character does not leave the map boundry
        if self.left < 0:
            self.left = 0
        elif self.right > constants.SCREEN_WIDTH - 1:
            self.right = constants.SCREEN_WIDTH -1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > constants.SCREEN_HEIGHT - 1:
            self.top = constants.SCREEN_HEIGHT -1



        