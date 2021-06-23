



from stickmanZ.__main__ import SCREEN_HEIGHT, SCREEN_WIDTH


MOVEMENT_SPEED = 5

class player_character(arcade.sprite):

    
    def __init__(self):
        super().__init__()

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        #Make sure character does not leave the map boundry
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH -1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT -1

    

    
