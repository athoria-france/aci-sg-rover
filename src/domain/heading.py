from enum import Enum, auto
from typing import assert_never

from src.domain.coordinates import Coordinates


class Heading(Enum):
    """The cardinal point a Rover faces."""

    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    def left(self) -> Heading:
        match self:
            case Heading.NORTH:
                return Heading.WEST
            case Heading.WEST:
                return Heading.SOUTH
            case Heading.SOUTH:
                return Heading.EAST
            case Heading.EAST:
                return Heading.NORTH
            case _:
                assert_never(self)

    def right(self) -> Heading:
        match self:
            case Heading.NORTH:
                return Heading.EAST
            case Heading.EAST:
                return Heading.SOUTH
            case Heading.SOUTH:
                return Heading.WEST
            case Heading.WEST:
                return Heading.NORTH
            case _:
                assert_never(self)

    def forward_from(self, origin: Coordinates) -> Coordinates:
        match self:
            case Heading.NORTH:
                return origin.shifted(0, 1)
            case Heading.EAST:
                return origin.shifted(1, 0)
            case Heading.SOUTH:
                return origin.shifted(0, -1)
            case Heading.WEST:
                return origin.shifted(-1, 0)
            case _:
                assert_never(self)
