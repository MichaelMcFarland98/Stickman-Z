import os

PATH = os.path.dirname(os.path.abspath(__file__))
HEAD, TAIL = os.path.split(PATH)
BACKGROUND = os.path.join(HEAD, 'assets', 'images', 'background.png')
# BACKGROUND = ":resources:images/backgrounds/abstract_1.jpg"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Stickman Z"
CHARACTER_SCALING = .5
TILE_SCALING = 0.5
STARTING_PLAYER_MOVEMENT_SPEED = 1
zombie_image = ":resources:images/animated_characters/zombie/zombie_idle.png"
SPRITE_SCALING_LASER = .8
BULLET_SPEED = 4
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * CHARACTER_SCALING)
RIGHT_FACING = 0
LEFT_FACING = 1
UPDATES_PER_FRAME = 5
