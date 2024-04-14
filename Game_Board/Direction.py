from enum import Enum


class Direction(Enum):
    """
    Enumeration of possible directions to move the pebbles
    """
    LEFT = -1
    RIGHT = 1

    def swap(self):
        """
        Swaps the direction around
        :return: Right if the direction was previously Left, Left if the direction was previously Right
        """
        if self == Direction.LEFT:
            return Direction.RIGHT
        else:
            return Direction.LEFT
