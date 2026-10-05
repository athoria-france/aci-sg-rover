from enum import Enum, auto


class Instruction(Enum):
    """An order executed by a Rover."""

    SPIN_LEFT = auto()
    SPIN_RIGHT = auto()
    MOVE = auto()
