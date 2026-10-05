import re
from collections.abc import Mapping

from src.adapters.mission_plan_parser import MissionPlanParser, MissionRejectedError
from src.domain.coordinates import Coordinates
from src.domain.errors import InvalidPlateauError
from src.domain.heading import Heading
from src.domain.instruction import Instruction
from src.domain.mission_plan import MissionPlan, RoverPlan
from src.domain.plateau import Plateau
from src.domain.position import Position


class MissionTextParser(MissionPlanParser):
    """Translates text format into a MissionPlan."""

    _PLATEAU: re.Pattern[str] = re.compile(r"(-?[0-9]+) (-?[0-9]+)")
    _POSITION: re.Pattern[str] = re.compile(r"(-?[0-9]+) (-?[0-9]+) (\S+)")
    _HEADINGS: Mapping[str, Heading] = {
        "N": Heading.NORTH,
        "E": Heading.EAST,
        "S": Heading.SOUTH,
        "W": Heading.WEST,
    }
    _INSTRUCTIONS: Mapping[str, Instruction] = {
        "L": Instruction.SPIN_LEFT,
        "R": Instruction.SPIN_RIGHT,
        "M": Instruction.MOVE,
    }

    def parse(self, text: str) -> MissionPlan:
        lines = text.splitlines()
        if not lines:
            raise MissionRejectedError(None, "missing plateau")
        plateau = self._parse_plateau(lines[0], 1)

        rovers: list[RoverPlan] = []
        index = 1
        while index < len(lines):
            position = self._parse_position(lines[index], index + 1)
            instructions_index = index + 1
            if instructions_index == len(lines):
                raise MissionRejectedError(instructions_index + 1, "missing instructions")
            instructions = self._parse_instructions(
                lines[instructions_index], instructions_index + 1
            )
            rovers.append(RoverPlan(position, instructions))
            index = instructions_index + 1

        return MissionPlan(plateau, tuple(rovers))

    def _parse_plateau(self, line: str, line_number: int) -> Plateau:
        self._reject_blank_line(line, line_number)
        match = self._PLATEAU.fullmatch(line)
        if match is None:
            raise MissionRejectedError(line_number, f"invalid plateau '{line}'")
        upper_right = Coordinates(
            self._parse_int(match[1], line_number), self._parse_int(match[2], line_number)
        )
        try:
            return Plateau(upper_right)
        except InvalidPlateauError as error:
            corner = error.upper_right
            raise MissionRejectedError(
                line_number, f"upper-right corner must not be negative, got {corner.x} {corner.y}"
            ) from error

    def _parse_position(self, line: str, line_number: int) -> Position:
        self._reject_blank_line(line, line_number)
        match = self._POSITION.fullmatch(line)
        if match is None:
            raise MissionRejectedError(line_number, f"invalid position '{line}'")
        heading = self._HEADINGS.get(match[3].upper())
        if heading is None:
            raise MissionRejectedError(line_number, f"invalid heading '{match[3]}'")
        coordinates = Coordinates(
            self._parse_int(match[1], line_number), self._parse_int(match[2], line_number)
        )
        return Position(coordinates, heading)

    def _parse_instructions(self, line: str, line_number: int) -> tuple[Instruction, ...]:
        instructions: list[Instruction] = []
        for letter in line:
            instruction = self._INSTRUCTIONS.get(letter.upper())
            if instruction is None:
                raise MissionRejectedError(line_number, f"invalid instruction '{letter}'")
            instructions.append(instruction)
        return tuple(instructions)

    @staticmethod
    def _reject_blank_line(line: str, line_number: int) -> None:
        if line == "":
            raise MissionRejectedError(line_number, "unexpected blank line")

    @staticmethod
    def _parse_int(digits: str, line_number: int) -> int:
        # int() refuses strings longer than sys.get_int_max_str_digits()
        try:
            return int(digits)
        except ValueError as error:
            raise MissionRejectedError(line_number, "coordinate too large") from error
