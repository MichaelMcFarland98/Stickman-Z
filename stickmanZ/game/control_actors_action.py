from game import constants
from game.action import Action
from game import constants


class ControlActorsAction(Action):
    """A code template for controlling actors. The responsibility of this
    class of objects is translate user input into some kind of intent.

    Stereotype:
        Controller

    Attributes:
        _input_service (InputService): An instance of InputService.
    """

    def __init__(self, input_service):
        """The class constructor.

        Args:
            input_service (InputService): An instance of InputService.
        """
        self._input_service = input_service

    def execute(self, cast):
        """Executes the action using the given actors.

        Args:
            cast (dict): The game actors {key: tag, value: list}.
        """
        direction = self._input_service.get_direction().scale(constants.PLAYER_MOVE_SCALE)
        player = cast["player"][0] # there's only one in the cast
        player.change_x = direction.get_x()
        player.change_y = direction.get_y()

        