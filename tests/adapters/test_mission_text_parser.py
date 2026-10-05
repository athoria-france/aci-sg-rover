import sys

import pytest

from src.adapters.mission_plan_parser import MissionRejectedError
from src.adapters.mission_text_parser import MissionTextParser
from src.domain.coordinates import Coordinates
from src.domain.heading import Heading
from src.domain.instruction import Instruction
from src.domain.mission_plan import MissionPlan, RoverPlan
from src.domain.plateau import Plateau
from src.domain.position import Position

_TOO_MANY_DIGITS = "9" * (sys.get_int_max_str_digits() + 1)


def test_parse_creates_plateau_and_each_rover_plan() -> None:
    # Arrange
    text = "5 5\n1 2 N\nLMR\n3 3 E\nMM\n"

    # Act
    plan = MissionTextParser().parse(text)

    # Assert
    assert plan == MissionPlan(
        Plateau(Coordinates(5, 5)),
        (
            RoverPlan(
                Position(Coordinates(1, 2), Heading.NORTH),
                (Instruction.SPIN_LEFT, Instruction.MOVE, Instruction.SPIN_RIGHT),
            ),
            RoverPlan(
                Position(Coordinates(3, 3), Heading.EAST),
                (Instruction.MOVE, Instruction.MOVE),
            ),
        ),
    )


def test_parse_ignores_case_of_heading_and_instructions() -> None:
    # Arrange
    text = "5 5\n1 2 w\nlrm\n"

    # Act
    plan = MissionTextParser().parse(text)

    # Assert
    assert plan.rovers == (
        RoverPlan(
            Position(Coordinates(1, 2), Heading.WEST),
            (Instruction.SPIN_LEFT, Instruction.SPIN_RIGHT, Instruction.MOVE),
        ),
    )


def test_parse_reads_blank_line_after_position_as_empty_instructions() -> None:
    # Arrange
    text = "5 5\n1 2 N\n\n3 3 E\nM\n"

    # Act
    plan = MissionTextParser().parse(text)

    # Assert
    assert plan.rovers == (
        RoverPlan(Position(Coordinates(1, 2), Heading.NORTH), ()),
        RoverPlan(Position(Coordinates(3, 3), Heading.EAST), (Instruction.MOVE,)),
    )


def test_parse_accepts_plateau_without_rovers() -> None:
    # Arrange
    text = "0 0\n"

    # Act
    plan = MissionTextParser().parse(text)

    # Assert
    assert plan == MissionPlan(Plateau(Coordinates(0, 0)), ())


def test_parse_accepts_negative_initial_position() -> None:
    # Arrange
    text = "5 5\n-1 -2 S\nM\n"

    # Act
    plan = MissionTextParser().parse(text)

    # Assert
    assert plan.rovers == (
        RoverPlan(Position(Coordinates(-1, -2), Heading.SOUTH), (Instruction.MOVE,)),
    )


def test_parse_accepts_windows_line_endings() -> None:
    # Arrange
    text = "5 5\r\n1 2 N\r\nM\r\n"

    # Act
    plan = MissionTextParser().parse(text)

    # Assert
    assert plan == MissionPlan(
        Plateau(Coordinates(5, 5)),
        (RoverPlan(Position(Coordinates(1, 2), Heading.NORTH), (Instruction.MOVE,)),),
    )


@pytest.mark.parametrize(
    ("text", "line_number", "reason"),
    [
        ("", None, "missing plateau"),
        ("\n5 5\n", 1, "unexpected blank line"),
        ("5 5\n\n1 2 N\nM\n", 2, "unexpected blank line"),
        ("5 5\n1 2 N\nM\n\n3 3 E\nM\n", 4, "unexpected blank line"),
        ("5 5\n1 2 N\nM\n\n", 4, "unexpected blank line"),
        ("5 5\n\n", 2, "unexpected blank line"),
        ("5\n", 1, "invalid plateau '5'"),
        ("a b\n", 1, "invalid plateau 'a b'"),
        ("5  5\n", 1, "invalid plateau '5  5'"),
        (" 5 5\n", 1, "invalid plateau ' 5 5'"),
        ("5 5 \n", 1, "invalid plateau '5 5 '"),
        ("-1 5\n", 1, "upper-right corner must not be negative, got -1 5"),
        (f"{_TOO_MANY_DIGITS} 5\n", 1, "coordinate too large"),
        (f"5 5\n1 -{_TOO_MANY_DIGITS} N\nM\n", 2, "coordinate too large"),
        ("5 5\n1 2\nM\n", 2, "invalid position '1 2'"),
        ("5 5\n1  2 N\nM\n", 2, "invalid position '1  2 N'"),
        ("5 5\n1 2 N \nM\n", 2, "invalid position '1 2 N '"),
        ("5 5\n1 2 X\nM\n", 2, "invalid heading 'X'"),
        ("5 5\n1 2 N\nLMX\n", 3, "invalid instruction 'X'"),
        ("5 5\n1 2 N\n LM\n", 3, "invalid instruction ' '"),
        ("5 5\n1 2 N\n", 3, "missing instructions"),
        ("5 5\n1 2 N\nM\n3 3 E", 5, "missing instructions"),
    ],
)
def test_parse_rejects_malformed_mission(text: str, line_number: int | None, reason: str) -> None:
    # Act & Assert
    with pytest.raises(MissionRejectedError) as rejection:
        MissionTextParser().parse(text)

    assert rejection.value.line_number == line_number
    assert rejection.value.reason == reason


def test_every_heading_and_instruction_can_be_read_from_text() -> None:
    # Act
    headings = set(MissionTextParser._HEADINGS.values())
    instructions = set(MissionTextParser._INSTRUCTIONS.values())

    # Assert
    assert headings == set(Heading)
    assert instructions == set(Instruction)
