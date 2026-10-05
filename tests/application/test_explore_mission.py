from collections.abc import Sequence

from src.application.ports.final_position_reporter import FinalPositionReporter
from src.application.ports.incident_reporter import IncidentReporter
from src.application.use_cases.explore_mission import ExploreMissionUseCase
from src.domain.coordinates import Coordinates
from src.domain.heading import Heading
from src.domain.incidents import LandingRejected, MissionIncident, MoveBlocked, Unavailability
from src.domain.instruction import Instruction
from src.domain.mission_plan import MissionPlan, RoverPlan
from src.domain.plateau import Plateau
from src.domain.position import Position
from src.domain.rover import RoverId


class InMemoryFinalPositionReporter(FinalPositionReporter):
    def __init__(self) -> None:
        self.reported: list[Position] = []

    def report(self, positions: Sequence[Position]) -> None:
        self.reported.extend(positions)


class InMemoryIncidentReporter(IncidentReporter):
    def __init__(self) -> None:
        self.reported: list[MissionIncident] = []

    def report(self, incidents: Sequence[MissionIncident]) -> None:
        self.reported.extend(incidents)


def test_execute_reports_final_positions_of_landed_rovers() -> None:
    # Arrange
    position_reporter = InMemoryFinalPositionReporter()
    incident_reporter = InMemoryIncidentReporter()
    use_case = ExploreMissionUseCase(position_reporter, incident_reporter)
    plan = MissionPlan(
        Plateau(Coordinates(5, 5)),
        (
            RoverPlan(
                Position(Coordinates(1, 2), Heading.NORTH),
                (Instruction.SPIN_LEFT, Instruction.MOVE),
            ),
            RoverPlan(
                Position(Coordinates(3, 3), Heading.EAST),
                (Instruction.MOVE, Instruction.SPIN_RIGHT),
            ),
        ),
    )

    # Act
    use_case.execute(plan)

    # Assert
    assert position_reporter.reported == [
        Position(Coordinates(0, 2), Heading.WEST),
        Position(Coordinates(4, 3), Heading.SOUTH),
    ]
    assert incident_reporter.reported == []


def test_execute_reports_incidents() -> None:
    # Arrange
    position_reporter = InMemoryFinalPositionReporter()
    incident_reporter = InMemoryIncidentReporter()
    use_case = ExploreMissionUseCase(position_reporter, incident_reporter)
    plan = MissionPlan(
        Plateau(Coordinates(5, 5)),
        (
            RoverPlan(Position(Coordinates(5, 5), Heading.NORTH), (Instruction.MOVE,)),
            RoverPlan(Position(Coordinates(9, 9), Heading.NORTH), ()),
        ),
    )

    # Act
    use_case.execute(plan)

    # Assert
    assert position_reporter.reported == [Position(Coordinates(5, 5), Heading.NORTH)]
    assert incident_reporter.reported == [
        LandingRejected(
            RoverId(2), Position(Coordinates(9, 9), Heading.NORTH), Unavailability.OUTSIDE_PLATEAU
        ),
        MoveBlocked(
            RoverId(1), Position(Coordinates(5, 5), Heading.NORTH), Unavailability.OUTSIDE_PLATEAU
        ),
    ]


def test_execute_without_rovers_reports_nothing() -> None:
    # Arrange
    position_reporter = InMemoryFinalPositionReporter()
    incident_reporter = InMemoryIncidentReporter()
    use_case = ExploreMissionUseCase(position_reporter, incident_reporter)
    plan = MissionPlan(Plateau(Coordinates(5, 5)), ())

    # Act
    use_case.execute(plan)

    # Assert
    assert position_reporter.reported == []
    assert incident_reporter.reported == []
