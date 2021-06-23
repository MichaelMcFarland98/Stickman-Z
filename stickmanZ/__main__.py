import arcade
from stickmanZ.game.display_screen import display_screen 

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Stickman Z"

def main():
    game = display_screen(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()
    

if __name__ == "__main__":
    main()

