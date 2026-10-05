from src.domain.coordinates import Coordinates


class DomainError(Exception):
    """Base class for every invariant violation."""


class InvalidPlateauError(DomainError):
    def __init__(self, upper_right: Coordinates) -> None:
        super().__init__(
            f"upper-right corner must not be negative, got {upper_right.x} {upper_right.y}"
        )
        self.upper_right = upper_right
