from dataclasses import dataclass

from src.domain.coordinates import Coordinates
from src.domain.errors import InvalidPlateauError


@dataclass(frozen=True)
class Plateau:
    """Rectangular area from (0, 0) to the upper-right corner, bounds included."""

    upper_right: Coordinates

    def __post_init__(self) -> None:
        if self.upper_right.x < 0 or self.upper_right.y < 0:
            raise InvalidPlateauError(self.upper_right)

    def contains(self, coordinates: Coordinates) -> bool:
        return 0 <= coordinates.x <= self.upper_right.x and 0 <= coordinates.y <= self.upper_right.y
