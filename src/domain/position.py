from dataclasses import dataclass

from src.domain.coordinates import Coordinates
from src.domain.heading import Heading


@dataclass(frozen=True)
class Position:
    """Where a Rover is (Coordinates) and where it faces (Heading)."""

    coordinates: Coordinates
    heading: Heading

    def spun_left(self) -> Position:
        return Position(self.coordinates, self.heading.left())

    def spun_right(self) -> Position:
        return Position(self.coordinates, self.heading.right())

    def next_coordinates(self) -> Coordinates:
        return self.heading.forward_from(self.coordinates)

    def moved_forward(self) -> Position:
        return Position(self.next_coordinates(), self.heading)
