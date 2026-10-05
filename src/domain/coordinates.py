from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinates:
    """Location on the Plateau axes: x grows towards East, y grows towards North."""

    x: int
    y: int

    def shifted(self, dx: int, dy: int) -> Coordinates:
        return Coordinates(self.x + dx, self.y + dy)
