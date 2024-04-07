from enum import Enum


class Direction(Enum):
    LEFT = -1
    RIGHT = 1

    def swap(self):
        if self == Direction.LEFT:
            return Direction.RIGHT
        else:
            return Direction.LEFT
