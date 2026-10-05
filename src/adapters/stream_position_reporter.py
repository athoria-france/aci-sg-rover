from collections.abc import Sequence
from typing import TextIO, assert_never

from src.application.ports.final_position_reporter import FinalPositionReporter
from src.domain.heading import Heading
from src.domain.position import Position


class StreamPositionReporter(FinalPositionReporter):
    """Writes each Final Position as 'x y H' on its own line."""

    def __init__(self, stream: TextIO) -> None:
        self._stream = stream

    def report(self, positions: Sequence[Position]) -> None:
        for position in positions:
            self._stream.write(f"{self._format_position(position)}\n")

    def _format_position(self, position: Position) -> str:
        coordinates = position.coordinates
        return f"{coordinates.x} {coordinates.y} {self._format_heading(position.heading)}"

    @staticmethod
    def _format_heading(heading: Heading) -> str:
        match heading:
            case Heading.NORTH:
                return "N"
            case Heading.EAST:
                return "E"
            case Heading.SOUTH:
                return "S"
            case Heading.WEST:
                return "W"
            case _:
                assert_never(heading)
