import arcade
import math
import random
from game.constants import *
from game.player import Player
from game.zombie import Zombie


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

        # Used in scrolling
        self.view_left = (PLAYING_FIELD_WIDTH - SCREEN_WIDTH) / 2
        self.view_bottom = (PLAYING_FIELD_HEIGHT - SCREEN_HEIGHT) / 2

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player(
            PLAYER_SPRITE, PLAYER_SCALING)
        self.player_sprite.center_x = PLAYING_FIELD_WIDTH / 2
        self.player_sprite.center_y = PLAYING_FIELD_HEIGHT / 2
        self.player_list.append(self.player_sprite)

        # Create the zombies
        for i in range(ZOMBIE_COUNT):

            # Create the zombies instance
            zombie_sprite = Zombie(
                ZOMBIE_SPRITE, ZOMBIE_SCALING)

            # Position the zombie
            section = random.randrange(1, 5)
            if section == 1:
                zombie_sprite.center_x = random.randrange(32, 160)
                zombie_sprite.center_y = random.randrange(1440, 1568)
            elif section == 2:
                zombie_sprite.center_x = random.randrange(3040, 3168)
                zombie_sprite.center_y = random.randrange(1440, 1568)
            elif section == 3:
                zombie_sprite.center_x = random.randrange(32, 160)
                zombie_sprite.center_y = random.randrange(32, 160)
            elif section == 4:
                zombie_sprite.center_x = random.randrange(3040, 3168)
                zombie_sprite.center_y = random.randrange(32, 160)

            # Add the zombie to the lists
            self.zombie_list.append(zombie_sprite)

        # for zombie in self.zombie_list:
        #     zombie.setup_other_zombies(zombie, self.zombie_list)

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
            # self.physics_engine_zombie.append(
            #     arcade.PhysicsEngineSimple(zombie, zombie.other_zombies))
            self.physics_engine_zombie.append(
                arcade.PhysicsEngineSimple(zombie, self.wall_list))

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
            if bullet.bottom > PLAYING_FIELD_HEIGHT or bullet.top < 0 or bullet.right < 0 or bullet.left > PLAYING_FIELD_WIDTH:
                bullet.remove_from_sprite_lists()

        # Call update to move the sprite
        self.player_list.update()
        self.bullet_list.update()

        self.physics_engine_player.update()

        for zombie_physics in self.physics_engine_zombie:
            zombie_physics.update()

        # --- Manage Scrolling ---

        changed = False

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN_WIDTH
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN_WIDTH
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN_HEIGHT
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN_HEIGHT
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

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
        dest_x = x + self.view_left
        dest_y = y + self.view_bottom

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

        dest_x = x + self.view_left
        dest_y = y + self.view_bottom

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
