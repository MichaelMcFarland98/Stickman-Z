import arcade
from game import constants

class weapon_room(arcade.Sprite):

    def __init__(self, sprite, scaling, name):
        """This class stores the weapons 
        and the name of the eapons so that we can better use it

        can create new weapons to pick up
        """
        super().__init__(sprite, scaling)
        self.name = name

    def get_name(self):
        return self.name