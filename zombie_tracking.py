import arcade
import math
import random
from game.constants import *


class Player(arcade.Sprite):

    def update(self):
        """ Move the player """

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


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

        if self.center_y < player_sprite.center_y:
            self.center_y += min(ZOMBIE_SPEED,
                                 player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(ZOMBIE_SPEED,
                                 self.center_y - player_sprite.center_y)

        if self.center_x < player_sprite.center_x:
            self.center_x += min(ZOMBIE_SPEED,
                                 player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(ZOMBIE_SPEED,
                                 self.center_x - player_sprite.center_x)

    def setup_other_zombies(self, zombie, zombie_list):
        """"""

        new_zombie_list = arcade.SpriteList()
        for x in zombie_list:
            if x != zombie:
                new_zombie_list.append(x)
        self.other_zombies = new_zombie_list


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None
        self.zombie_list = None
        self.bullet_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.score_text = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player(
            PLAYER_SPRITE, PLAYER_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)

        # Create the zombies
        for i in range(ZOMBIE_COUNT):

            # Create the zombies instance
            zombie = Zombie(
                ZOMBIE_SPRITE, ZOMBIE_SCALING)

            # Position the zombie
            zombie.center_x = random.randrange(SCREEN_WIDTH)
            zombie.center_y = random.randrange(120, SCREEN_HEIGHT)

            # Add the zombie to the lists
            self.zombie_list.append(zombie)

        for zombie in self.zombie_list:
            zombie.setup_other_zombies(zombie, self.zombie_list)

        my_map = arcade.tilemap.read_tmx(MAP_PATH)

        self.floor_list = arcade.tilemap.process_layer(map_object=my_map,
                                                       layer_name=LAYER_FLOOR,
                                                       scaling=TILE_SCALING,
                                                       use_spatial_hash=True)

        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=LAYER_WALLS,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        self.physics_engine_player = arcade.PhysicsEngineSimple(
            self.player_sprite, self.wall_list)

        self.physics_engine_zombie = []

        for zombie in self.zombie_list:
            zombie_collision_list = zombie.other_zombies
            self.physics_engine_zombie.append(
                arcade.PhysicsEngineSimple(zombie, zombie_collision_list))

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.floor_list.draw()
        self.wall_list.draw()
        self.player_list.draw()
        self.zombie_list.draw()
        self.bullet_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_SPEED

        for zombie in self.zombie_list:
            zombie.follow_sprite(self.player_sprite)

        # Loop through each bullet
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a zombie
            hit_list = arcade.check_for_collision_with_list(
                bullet, self.zombie_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every zombie we hit, add to the score and remove the zombie
            for zombie in hit_list:
                zombie.remove_from_sprite_lists()
                self.score += 1

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()

        # Call update to move the sprite
        self.player_list.update()
        self.bullet_list.update()

        self.physics_engine_player.update()

        for zombie_physics in self.physics_engine_zombie:
            zombie_physics.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        # Create a bullet
        bullet = arcade.Sprite(
            ":resources:images/space_shooter/laserBlue01.png", BULLET_SCALING)

        # Position the bullet at the player's current location
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get from the mouse the destination location for the bullet
        dest_x = x
        dest_y = y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying
        # sideways.
        bullet.angle = math.degrees(angle)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ Handle Mouse Motion """

        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y

        dest_x = x
        dest_y = y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        self.player_sprite.angle = math.degrees(angle)-90


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH,
                    SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
