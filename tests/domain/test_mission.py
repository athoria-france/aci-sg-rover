from src.domain.coordinates import Coordinates
from src.domain.heading import Heading
from src.domain.incidents import LandingRejected, MoveBlocked, Unavailability
from src.domain.instruction import Instruction
from src.domain.mission import Mission
from src.domain.mission_plan import MissionPlan, RoverPlan
from src.domain.plateau import Plateau
from src.domain.position import Position
from src.domain.rover import RoverId


def test_explore_executes_instructions_of_each_rover() -> None:
    # Arrange
    mission = Mission(Plateau(Coordinates(5, 5)))
    mission.land(
        RoverId(1),
        Position(Coordinates(1, 2), Heading.NORTH),
        (
            Instruction.SPIN_LEFT,
            Instruction.MOVE,
            Instruction.SPIN_LEFT,
            Instruction.MOVE,
            Instruction.SPIN_LEFT,
            Instruction.MOVE,
            Instruction.SPIN_LEFT,
            Instruction.MOVE,
            Instruction.MOVE,
        ),
    )
    mission.land(
        RoverId(2),
        Position(Coordinates(3, 3), Heading.EAST),
        (
            Instruction.MOVE,
            Instruction.MOVE,
            Instruction.SPIN_RIGHT,
            Instruction.MOVE,
            Instruction.MOVE,
            Instruction.SPIN_RIGHT,
            Instruction.MOVE,
            Instruction.SPIN_RIGHT,
            Instruction.SPIN_RIGHT,
            Instruction.MOVE,
        ),
    )

    # Act
    mission.explore()

    # Assert
    assert mission.final_positions() == (
        Position(Coordinates(1, 3), Heading.NORTH),
        Position(Coordinates(5, 1), Heading.EAST),
    )
    assert mission.pull_incidents() == ()


def test_rover_without_instructions_stays_at_initial_position() -> None:
    # Arrange
    mission = Mission(Plateau(Coordinates(5, 5)))
    mission.land(RoverId(1), Position(Coordinates(2, 2), Heading.SOUTH), ())

    # Act
    mission.explore()

    # Assert
    assert mission.final_positions() == (Position(Coordinates(2, 2), Heading.SOUTH),)


def test_landing_outside_plateau_is_rejected() -> None:
    # Arrange
    mission = Mission(Plateau(Coordinates(5, 5)))

    # Act
    mission.land(RoverId(1), Position(Coordinates(6, 2), Heading.NORTH), (Instruction.MOVE,))

    # Assert
    assert mission.final_positions() == ()
    assert mission.pull_incidents() == (
        LandingRejected(
            RoverId(1), Position(Coordinates(6, 2), Heading.NORTH), Unavailability.OUTSIDE_PLATEAU
        ),
    )


def test_landing_with_negative_coordinates_is_rejected() -> None:
    # Arrange
    mission = Mission(Plateau(Coordinates(5, 5)))

    # Act
    mission.land(RoverId(1), Position(Coordinates(-1, 2), Heading.NORTH), (Instruction.MOVE,))

    # Assert
    assert mission.final_positions() == ()
    assert mission.pull_incidents() == (
        LandingRejected(
            RoverId(1), Position(Coordinates(-1, 2), Heading.NORTH), Unavailability.OUTSIDE_PLATEAU
        ),
    )


def test_landing_on_cell_of_previously_landed_rover_is_rejected() -> None:
    # Arrange
    mission = Mission(Plateau(Coordinates(5, 5)))
    mission.land(RoverId(1), Position(Coordinates(1, 1), Heading.NORTH), ())

    # Act
    mission.land(RoverId(2), Position(Coordinates(1, 1), Heading.EAST), ())

    # Assert
    assert mission.final_positions() == (Position(Coordinates(1, 1), Heading.NORTH),)
    assert mission.pull_incidents() == (
        LandingRejected(
            RoverId(2), Position(Coordinates(1, 1), Heading.EAST), Unavailability.OCCUPIED
        ),
    )


def test_rejected_rover_is_not_an_obstacle() -> None:
    # Arrange
    mission = Mission(Plateau(Coordinates(5, 5)))
    mission.land(
        RoverId(1),
        Position(Coordinates(1, 1), Heading.NORTH),
        (Instruction.MOVE, Instruction.SPIN_RIGHT, Instruction.SPIN_RIGHT, Instruction.MOVE),
    )
    mission.land(RoverId(2), Position(Coordinates(1, 1), Heading.NORTH), ())
    mission.pull_incidents()

    # Act
    mission.explore()

    # Assert
    assert mission.final_positions() == (Position(Coordinates(1, 1), Heading.SOUTH),)
    assert mission.pull_incidents() == ()


def test_move_beyond_plateau_edge_is_blocked_and_rover_goes_on() -> None:
    # Arrange
    mission = Mission(Plateau(Coordinates(5, 5)))
    mission.land(
        RoverId(1),
        Position(Coordinates(0, 5), Heading.NORTH),
        (Instruction.MOVE, Instruction.SPIN_RIGHT, Instruction.MOVE),
    )

    # Act
    mission.explore()

    # Assert
    assert mission.final_positions() == (Position(Coordinates(1, 5), Heading.EAST),)
    assert mission.pull_incidents() == (
        MoveBlocked(
            RoverId(1), Position(Coordinates(0, 5), Heading.NORTH), Unavailability.OUTSIDE_PLATEAU
        ),
    )


def test_move_onto_rover_that_has_not_moved_yet_is_blocked() -> None:
    # Arrange
    mission = Mission(Plateau(Coordinates(5, 5)))
    mission.land(RoverId(1), Position(Coordinates(1, 1), Heading.EAST), (Instruction.MOVE,))
    mission.land(RoverId(2), Position(Coordinates(2, 1), Heading.NORTH), ())

    # Act
    mission.explore()

    # Assert
    assert mission.final_positions() == (
        Position(Coordinates(1, 1), Heading.EAST),
        Position(Coordinates(2, 1), Heading.NORTH),
    )
    assert mission.pull_incidents() == (
        MoveBlocked(RoverId(1), Position(Coordinates(1, 1), Heading.EAST), Unavailability.OCCUPIED),
    )


def test_move_onto_final_position_of_previous_rover_is_blocked() -> None:
    # Arrange
    mission = Mission(Plateau(Coordinates(5, 5)))
    mission.land(RoverId(1), Position(Coordinates(1, 1), Heading.NORTH), (Instruction.MOVE,))
    mission.land(
        RoverId(2), Position(Coordinates(1, 3), Heading.SOUTH), (Instruction.MOVE, Instruction.MOVE)
    )

    # Act
    mission.explore()

    # Assert
    assert mission.final_positions() == (
        Position(Coordinates(1, 2), Heading.NORTH),
        Position(Coordinates(1, 3), Heading.SOUTH),
    )
    assert mission.pull_incidents() == (
        MoveBlocked(
            RoverId(2), Position(Coordinates(1, 3), Heading.SOUTH), Unavailability.OCCUPIED
        ),
        MoveBlocked(
            RoverId(2), Position(Coordinates(1, 3), Heading.SOUTH), Unavailability.OCCUPIED
        ),
    )


def test_rovers_explore_sequentially() -> None:
    # Arrange
    mission = Mission(Plateau(Coordinates(5, 5)))
    mission.land(
        RoverId(1),
        Position(Coordinates(1, 1), Heading.NORTH),
        (Instruction.SPIN_LEFT, Instruction.SPIN_RIGHT, Instruction.MOVE),
    )
    mission.land(RoverId(2), Position(Coordinates(0, 1), Heading.EAST), (Instruction.MOVE,))

    # Act
    mission.explore()

    # Assert
    assert mission.final_positions() == (
        Position(Coordinates(1, 2), Heading.NORTH),
        Position(Coordinates(1, 1), Heading.EAST),
    )
    assert mission.pull_incidents() == ()


def test_pull_incidents_clears_recorded_incidents() -> None:
    # Arrange
    mission = Mission(Plateau(Coordinates(5, 5)))
    mission.land(RoverId(1), Position(Coordinates(9, 9), Heading.NORTH), ())
    mission.pull_incidents()

    # Act
    incidents = mission.pull_incidents()

    # Assert
    assert incidents == ()


def test_from_plan_identifies_rovers_by_their_order_in_plan() -> None:
    # Arrange
    plan = MissionPlan(
        Plateau(Coordinates(5, 5)),
        (
            RoverPlan(Position(Coordinates(1, 1), Heading.NORTH), ()),
            RoverPlan(Position(Coordinates(9, 9), Heading.NORTH), ()),
            RoverPlan(Position(Coordinates(1, 1), Heading.EAST), ()),
        ),
    )

    # Act
    mission = Mission.from_plan(plan)

    # Assert
    assert mission.final_positions() == (Position(Coordinates(1, 1), Heading.NORTH),)
    assert mission.pull_incidents() == (
        LandingRejected(
            RoverId(2), Position(Coordinates(9, 9), Heading.NORTH), Unavailability.OUTSIDE_PLATEAU
        ),
        LandingRejected(
            RoverId(3), Position(Coordinates(1, 1), Heading.EAST), Unavailability.OCCUPIED
        ),
    )
