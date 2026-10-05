from dataclasses import dataclass

from src.domain.coordinates import Coordinates
from src.domain.instruction import Instruction
from src.domain.position import Position


@dataclass(frozen=True)
class RoverId:
    """Rank of the Rover in the Mission, starting at 1."""

    value: int


class Rover:
    """Landed on the Plateau, it executes its Instructions during the Mission."""

    def __init__(
        self, rover_id: RoverId, position: Position, instructions: tuple[Instruction, ...]
    ) -> None:
        self._id = rover_id
        self._position = position
        self._instructions = instructions

    @property
    def id(self) -> RoverId:
        return self._id

    @property
    def position(self) -> Position:
        return self._position

    @property
    def instructions(self) -> tuple[Instruction, ...]:
        return self._instructions

    def spin_left(self) -> None:
        self._position = self._position.spun_left()

    def spin_right(self) -> None:
        self._position = self._position.spun_right()

    def next_coordinates(self) -> Coordinates:
        return self._position.next_coordinates()

    def move_forward(self) -> None:
        self._position = self._position.moved_forward()
