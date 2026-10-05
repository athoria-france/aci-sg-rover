import pytest

from src.domain.coordinates import Coordinates
from src.domain.heading import Heading


@pytest.mark.parametrize(
    ("heading", "expected"),
    [
        (Heading.NORTH, Heading.WEST),
        (Heading.WEST, Heading.SOUTH),
        (Heading.SOUTH, Heading.EAST),
        (Heading.EAST, Heading.NORTH),
    ],
)
def test_left_rotates_ninety_degrees_counterclockwise(heading: Heading, expected: Heading) -> None:
    # Act
    result = heading.left()

    # Assert
    assert result is expected


@pytest.mark.parametrize(
    ("heading", "expected"),
    [
        (Heading.NORTH, Heading.EAST),
        (Heading.EAST, Heading.SOUTH),
        (Heading.SOUTH, Heading.WEST),
        (Heading.WEST, Heading.NORTH),
    ],
)
def test_right_rotates_ninety_degrees_clockwise(heading: Heading, expected: Heading) -> None:
    # Act
    result = heading.right()

    # Assert
    assert result is expected


@pytest.mark.parametrize(
    ("heading", "expected"),
    [
        (Heading.NORTH, Coordinates(1, 3)),
        (Heading.EAST, Coordinates(2, 2)),
        (Heading.SOUTH, Coordinates(1, 1)),
        (Heading.WEST, Coordinates(0, 2)),
    ],
)
def test_forward_from_returns_adjacent_coordinates_in_heading_direction(
    heading: Heading, expected: Coordinates
) -> None:
    # Arrange
    origin = Coordinates(1, 2)

    # Act
    result = heading.forward_from(origin)

    # Assert
    assert result == expected
