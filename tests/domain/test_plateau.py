import pytest

from src.domain.coordinates import Coordinates
from src.domain.errors import InvalidPlateauError
from src.domain.plateau import Plateau


@pytest.mark.parametrize("upper_right", [Coordinates(-1, 5), Coordinates(5, -1)])
def test_plateau_with_negative_upper_right_corner_is_invalid(upper_right: Coordinates) -> None:
    # Act & Assert
    with pytest.raises(InvalidPlateauError):
        Plateau(upper_right)


def test_single_cell_plateau_can_be_created() -> None:
    # Arrange
    upper_right = Coordinates(0, 0)

    # Act
    plateau = Plateau(upper_right)

    # Assert
    assert plateau.upper_right == Coordinates(0, 0)


@pytest.mark.parametrize(
    "coordinates",
    [Coordinates(0, 0), Coordinates(5, 3), Coordinates(0, 3), Coordinates(5, 0), Coordinates(2, 1)],
)
def test_plateau_contains_coordinates_within_inclusive_bounds(coordinates: Coordinates) -> None:
    # Arrange
    plateau = Plateau(Coordinates(5, 3))

    # Act
    contained = plateau.contains(coordinates)

    # Assert
    assert contained


@pytest.mark.parametrize(
    "coordinates",
    [Coordinates(-1, 0), Coordinates(0, -1), Coordinates(6, 3), Coordinates(5, 4)],
)
def test_plateau_does_not_contain_coordinates_outside_bounds(coordinates: Coordinates) -> None:
    # Arrange
    plateau = Plateau(Coordinates(5, 3))

    # Act
    contained = plateau.contains(coordinates)

    # Assert
    assert not contained
