import arcade
from game import constants

class HandleCollisions:

    def __init__(self):
        self.center_x = None
        self.center_y = None
        self.did_hit = False


    def zombie_player_collision(self, player_sprites):
        """
        When zombie hits player, player loses hp
        """

        player = player_sprites['player'][0]
        player_sprite = player[0]
        zombie_list = player_sprites['zombie'][0]

        #if the player is hit by the zombie reduce the player's health
        for zombie in zombie_list:

            hit_list = arcade.check_for_collision_with_list(zombie, player)

            if len(hit_list) > 0:
                player_sprite.player_damage(zombie.get_damage())
                zombie.set_hit_player()

    
