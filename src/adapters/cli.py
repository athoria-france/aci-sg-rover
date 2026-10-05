from collections.abc import Sequence
from pathlib import Path

from src.adapters.mission_plan_parser import MissionPlanParser, MissionRejectedError
from src.adapters.stream_logger import Severity, StreamLogger
from src.application.ports.explore_mission import ExploreMission


class CommandLineInterface:
    """Driving adapter: reads the Mission file given on the command line and explores it."""

    EXIT_SUCCESS: int = 0
    EXIT_MISSION_REJECTED: int = 1
    EXIT_USAGE: int = 2

    _USAGE: str = "usage: rover.py <input-file>"

    def __init__(
        self, logger: StreamLogger, parser: MissionPlanParser, explore_mission: ExploreMission
    ) -> None:
        self._logger = logger
        self._parser = parser
        self._explore_mission = explore_mission

    def run(self, args: Sequence[str]) -> int:
        if len(args) != 1:
            self._logger.log(Severity.NONE, self._USAGE)
            return self.EXIT_USAGE

        path = Path(args[0])
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            self._logger.log(
                Severity.ERROR, f"Cannot read '{path}': {self._describe_read_error(error)}"
            )
            return self.EXIT_MISSION_REJECTED

        try:
            plan = self._parser.parse(text)
        except MissionRejectedError as error:
            self._logger.log(Severity.ERROR, self._format_rejection(error))
            return self.EXIT_MISSION_REJECTED

        self._explore_mission.execute(plan)
        return self.EXIT_SUCCESS

    @staticmethod
    def _describe_read_error(error: OSError | UnicodeDecodeError) -> str:
        if isinstance(error, UnicodeDecodeError):
            return "not a valid UTF-8 text file"
        return error.strerror or str(error)

    @staticmethod
    def _format_rejection(error: MissionRejectedError) -> str:
        if error.line_number is None:
            return error.reason
        return f"Line {error.line_number} - {error.reason}"
