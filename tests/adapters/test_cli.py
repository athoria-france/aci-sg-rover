import io
from pathlib import Path

import pytest

from src.adapters.cli import CommandLineInterface
from src.adapters.mission_text_parser import MissionTextParser
from src.adapters.stream_logger import StreamLogger
from src.application.ports.explore_mission import ExploreMission
from src.domain.coordinates import Coordinates
from src.domain.heading import Heading
from src.domain.instruction import Instruction
from src.domain.mission_plan import MissionPlan, RoverPlan
from src.domain.plateau import Plateau
from src.domain.position import Position


class SpyExploreMission(ExploreMission):
    def __init__(self) -> None:
        self.executed: list[MissionPlan] = []

    def execute(self, plan: MissionPlan) -> None:
        self.executed.append(plan)


def _write_input(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "input.txt"
    path.write_text(content, encoding="utf-8")
    return path


def test_run_explores_the_mission_read_from_the_file(tmp_path: Path) -> None:
    # Arrange
    path = _write_input(tmp_path, "5 5\n1 2 N\nLM\n")
    stderr = io.StringIO()
    explore_mission = SpyExploreMission()

    # Act
    exit_code = CommandLineInterface(
        StreamLogger(stderr), MissionTextParser(), explore_mission
    ).run([str(path)])

    # Assert
    assert exit_code == CommandLineInterface.EXIT_SUCCESS
    assert explore_mission.executed == [
        MissionPlan(
            Plateau(Coordinates(5, 5)),
            (
                RoverPlan(
                    Position(Coordinates(1, 2), Heading.NORTH),
                    (Instruction.SPIN_LEFT, Instruction.MOVE),
                ),
            ),
        )
    ]
    assert stderr.getvalue() == ""


@pytest.mark.parametrize("args", [[], ["a.txt", "b.txt"]])
def test_run_with_wrong_number_of_arguments_prints_usage(args: list[str]) -> None:
    # Arrange
    stderr = io.StringIO()
    explore_mission = SpyExploreMission()

    # Act
    exit_code = CommandLineInterface(
        StreamLogger(stderr), MissionTextParser(), explore_mission
    ).run(args)

    # Assert
    assert exit_code == CommandLineInterface.EXIT_USAGE
    assert stderr.getvalue() == "usage: rover.py <input-file>\n"
    assert explore_mission.executed == []


def test_run_with_missing_file_rejects_the_mission(tmp_path: Path) -> None:
    # Arrange
    path = tmp_path / "missing.txt"
    stderr = io.StringIO()
    explore_mission = SpyExploreMission()

    # Act
    exit_code = CommandLineInterface(
        StreamLogger(stderr), MissionTextParser(), explore_mission
    ).run([str(path)])

    # Assert
    assert exit_code == CommandLineInterface.EXIT_MISSION_REJECTED
    assert stderr.getvalue().startswith(f"[ERROR] Cannot read '{path}': ")
    assert explore_mission.executed == []


def test_run_with_non_utf8_file_rejects_the_mission(tmp_path: Path) -> None:
    # Arrange
    path = tmp_path / "input.txt"
    path.write_bytes(b"\xff\xfe5 5\n")
    stderr = io.StringIO()
    explore_mission = SpyExploreMission()

    # Act
    exit_code = CommandLineInterface(
        StreamLogger(stderr), MissionTextParser(), explore_mission
    ).run([str(path)])

    # Assert
    assert exit_code == CommandLineInterface.EXIT_MISSION_REJECTED
    assert stderr.getvalue() == f"[ERROR] Cannot read '{path}': not a valid UTF-8 text file\n"
    assert explore_mission.executed == []


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("5 5\n1 2 N\nLM\n3 3 X\nM\n", "[ERROR] Line 4 - invalid heading 'X'\n"),
        ("", "[ERROR] missing plateau\n"),
    ],
)
def test_run_with_malformed_file_rejects_the_mission(
    tmp_path: Path, content: str, expected: str
) -> None:
    # Arrange
    path = _write_input(tmp_path, content)
    stderr = io.StringIO()
    explore_mission = SpyExploreMission()

    # Act
    exit_code = CommandLineInterface(
        StreamLogger(stderr), MissionTextParser(), explore_mission
    ).run([str(path)])

    # Assert
    assert exit_code == CommandLineInterface.EXIT_MISSION_REJECTED
    assert stderr.getvalue() == expected
    assert explore_mission.executed == []
