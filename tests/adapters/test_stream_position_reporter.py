import io

import pytest

from src.adapters.stream_position_reporter import StreamPositionReporter
from src.domain.coordinates import Coordinates
from src.domain.heading import Heading
from src.domain.position import Position


def test_report_writes_one_line_per_final_position() -> None:
    # Arrange
    stream = io.StringIO()
    reporter = StreamPositionReporter(stream)

    # Act
    reporter.report(
        [Position(Coordinates(1, 3), Heading.NORTH), Position(Coordinates(5, 1), Heading.EAST)]
    )

    # Assert
    assert stream.getvalue() == "1 3 N\n5 1 E\n"


@pytest.mark.parametrize(
    ("heading", "letter"),
    [(Heading.NORTH, "N"), (Heading.EAST, "E"), (Heading.SOUTH, "S"), (Heading.WEST, "W")],
)
def test_report_writes_heading_as_its_letter(heading: Heading, letter: str) -> None:
    # Arrange
    stream = io.StringIO()
    reporter = StreamPositionReporter(stream)

    # Act
    reporter.report([Position(Coordinates(-1, 3), heading)])

    # Assert
    assert stream.getvalue() == f"-1 3 {letter}\n"


def test_report_without_positions_writes_nothing() -> None:
    # Arrange
    stream = io.StringIO()
    reporter = StreamPositionReporter(stream)

    # Act
    reporter.report([])

    # Assert
    assert stream.getvalue() == ""
