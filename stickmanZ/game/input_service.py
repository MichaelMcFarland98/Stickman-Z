import arcade
import math
import random


class Input_service:

    def __init__(self):
        pass

    def on_release(self, key, modifiers, player_sprites):
        player_sprite = player_sprites["player"][0][0]
        if key == arcade.key.UP or key == arcade.key.W:
            player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            player_sprite.change_x = 0
        return player_sprite

    def on_press(self, key, modifiers, player_sprites, movement_speed):
        player_sprite = player_sprites["player"][0][0]
        if key == arcade.key.UP or key == arcade.key.W:
            player_sprite.change_y = movement_speed
        elif key == arcade.key.DOWN or key == arcade.key.S:
            player_sprite.change_y = -movement_speed
        elif key == arcade.key.LEFT or key == arcade.key.A:
            player_sprite.change_x = -movement_speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            player_sprite.change_x = movement_speed
        return player_sprite

    def on_click(self, x, y, button, modifiers, player_sprites, SPRITE_SCALING_LASER):
        """ Called whenever the mouse button is clicked. """

        player_sprite = player_sprites["player"][0][0]
        start_x = player_sprite.center_x
        start_y = player_sprite.center_y

        return player_sprites
