from src.domain.coordinates import Coordinates
from src.domain.heading import Heading
from src.domain.instruction import Instruction
from src.domain.position import Position
from src.domain.rover import Rover, RoverId


def test_spin_left_turns_rover_without_moving_it() -> None:
    # Arrange
    rover = Rover(RoverId(1), Position(Coordinates(1, 2), Heading.NORTH), (Instruction.MOVE,))

    # Act
    rover.spin_left()

    # Assert
    assert rover.position == Position(Coordinates(1, 2), Heading.WEST)


def test_spin_right_turns_rover_without_moving_it() -> None:
    # Arrange
    rover = Rover(RoverId(1), Position(Coordinates(1, 2), Heading.NORTH), (Instruction.MOVE,))

    # Act
    rover.spin_right()

    # Assert
    assert rover.position == Position(Coordinates(1, 2), Heading.EAST)


def test_move_forward_advances_one_cell_and_keeps_heading() -> None:
    # Arrange
    rover = Rover(RoverId(1), Position(Coordinates(1, 2), Heading.EAST), (Instruction.MOVE,))

    # Act
    rover.move_forward()

    # Assert
    assert rover.position == Position(Coordinates(2, 2), Heading.EAST)


def test_next_coordinates_returns_cell_in_front_of_rover_without_moving_it() -> None:
    # Arrange
    rover = Rover(RoverId(1), Position(Coordinates(1, 2), Heading.SOUTH), (Instruction.MOVE,))

    # Act
    next_coordinates = rover.next_coordinates()

    # Assert
    assert next_coordinates == Coordinates(1, 1)
    assert rover.position == Position(Coordinates(1, 2), Heading.SOUTH)
