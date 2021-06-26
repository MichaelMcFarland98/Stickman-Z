import arcade
from game.input_service import InputService
from game.output_service import OutputService
# from game.display_screen import display_screen 
from game.player import Player
from game import constants
from game.draw_actors_action import DrawActorsAction
from game.control_actors_action import ControlActorsAction
from game.move_actors_action import MoveActorsAction
from game.stickmanz import Stickmanz
from game.point import Point


def main():
    cast = {}

    player = Player()
    cast["player"] = [player]
    # game = display_screen(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    
    script = {}
    input_service = InputService()
    output_service = OutputService()

    control_actors_action = ControlActorsAction(input_service)
    move_actors_action = MoveActorsAction()
    # handle_collisions_action = HandleCollisionsAction()
    draw_actors_action = DrawActorsAction(output_service)

    script["input"] = [control_actors_action]
    script["update"] = [move_actors_action] #add handle_collisions_actor later
    script["output"] = [draw_actors_action]

    stickmanz = Stickmanz(cast, script, input_service)
    stickmanz.setup()
    arcade.run()
    

if __name__ == "__main__":
    main()

