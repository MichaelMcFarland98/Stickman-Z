import arcade
from game.constants import *


class Player(arcade.Sprite):

    def update(self):
        """ Move the player """

        self.center_x += self.change_x
        self.center_y += self.change_y

       # Check bounds
        if self.left < 0:
            self.left = 0
        elif self.right > PLAYING_FIELD_WIDTH - 1:
            self.right = PLAYING_FIELD_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > PLAYING_FIELD_HEIGHT - 1:
            self.top = PLAYING_FIELD_HEIGHT - 1
