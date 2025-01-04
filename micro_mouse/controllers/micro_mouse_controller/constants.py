from enum import Enum

class Direction(Enum):
    STRAIGHT = 0
    RIGHT = 1
    LEFT = -1
    TURN_OVER = 2