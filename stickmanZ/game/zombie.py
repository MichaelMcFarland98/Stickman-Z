import arcade
import math
import random
from game.constants import *


class Zombie(arcade.Sprite):
    """
    This class represents the Zombies on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def __init__(self, sprite, scaling):
        self.other_zombies = arcade.SpriteList()
        super().__init__(sprite, scaling)

    def follow_sprite(self, player_sprite):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of ZOMBIE_SPEED.
        """

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the player
        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            self.change_x = math.cos(angle) * ZOMBIE_SPEED
            self.change_y = math.sin(angle) * ZOMBIE_SPEED

    def setup_other_zombies(self, zombie, zombie_list):
        """"""

        new_zombie_list = arcade.SpriteList()
        for x in zombie_list:
            if x != zombie:
                new_zombie_list.append(x)
        self.other_zombies = new_zombie_list
