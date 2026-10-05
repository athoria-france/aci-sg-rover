import io

import pytest

from src.adapters.stream_incident_reporter import StreamIncidentReporter
from src.adapters.stream_logger import StreamLogger
from src.domain.coordinates import Coordinates
from src.domain.heading import Heading
from src.domain.incidents import LandingRejected, MissionIncident, MoveBlocked, Unavailability
from src.domain.position import Position
from src.domain.rover import RoverId


@pytest.mark.parametrize(
    ("incident", "expected"),
    [
        (
            LandingRejected(
                RoverId(2),
                Position(Coordinates(6, 6), Heading.NORTH),
                Unavailability.OUTSIDE_PLATEAU,
            ),
            "[WARN] Rover #2 - Landing rejected (6 6 N): outside plateau\n",
        ),
        (
            LandingRejected(
                RoverId(3), Position(Coordinates(1, 1), Heading.EAST), Unavailability.OCCUPIED
            ),
            "[WARN] Rover #3 - Landing rejected (1 1 E): occupied by another rover\n",
        ),
        (
            MoveBlocked(
                RoverId(1),
                Position(Coordinates(5, 5), Heading.NORTH),
                Unavailability.OUTSIDE_PLATEAU,
            ),
            "[WARN] Rover #1 - Move blocked (5 5 N): outside plateau\n",
        ),
        (
            MoveBlocked(
                RoverId(1), Position(Coordinates(5, 5), Heading.WEST), Unavailability.OCCUPIED
            ),
            "[WARN] Rover #1 - Move blocked (5 5 W): occupied by another rover\n",
        ),
        (
            MoveBlocked(
                RoverId(4),
                Position(Coordinates(0, 0), Heading.SOUTH),
                Unavailability.OUTSIDE_PLATEAU,
            ),
            "[WARN] Rover #4 - Move blocked (0 0 S): outside plateau\n",
        ),
    ],
)
def test_report_writes_one_warning_per_incident(incident: MissionIncident, expected: str) -> None:
    # Arrange
    stream = io.StringIO()
    reporter = StreamIncidentReporter(StreamLogger(stream))

    # Act
    reporter.report([incident])

    # Assert
    assert stream.getvalue() == expected


def test_report_without_incidents_writes_nothing() -> None:
    # Arrange
    stream = io.StringIO()
    reporter = StreamIncidentReporter(StreamLogger(stream))

    # Act
    reporter.report([])

    # Assert
    assert stream.getvalue() == ""
