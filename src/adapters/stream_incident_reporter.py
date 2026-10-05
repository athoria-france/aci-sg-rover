from collections.abc import Sequence
from typing import assert_never

from src.adapters.stream_logger import Severity, StreamLogger
from src.application.ports.incident_reporter import IncidentReporter
from src.domain.heading import Heading
from src.domain.incidents import LandingRejected, MissionIncident, MoveBlocked, Unavailability
from src.domain.position import Position


class StreamIncidentReporter(IncidentReporter):
    """Logs each Mission Incident as a warning."""

    def __init__(self, logger: StreamLogger) -> None:
        self._logger = logger

    def report(self, incidents: Sequence[MissionIncident]) -> None:
        for incident in incidents:
            self._logger.log(Severity.WARNING, self._format_incident(incident))

    def _format_incident(self, incident: MissionIncident) -> str:
        match incident:
            case LandingRejected():
                event = "Landing rejected"
            case MoveBlocked():
                event = "Move blocked"
            case _:
                assert_never(incident)
        return (
            f"Rover #{incident.rover_id.value} - {event} "
            f"({self._format_position(incident.position)}): "
            f"{self._format_reason(incident.reason)}"
        )

    @staticmethod
    def _format_reason(reason: Unavailability) -> str:
        match reason:
            case Unavailability.OUTSIDE_PLATEAU:
                return "outside plateau"
            case Unavailability.OCCUPIED:
                return "occupied by another rover"
            case _:
                assert_never(reason)

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
