from abc import ABC, abstractmethod

from src.domain.mission_plan import MissionPlan


class MissionRejectedError(Exception):
    """The Mission cannot be read: nothing is explored, nothing is reported."""

    def __init__(self, line_number: int | None, reason: str) -> None:
        super().__init__(reason if line_number is None else f"line {line_number}: {reason}")
        self.line_number = line_number
        self.reason = reason


class MissionPlanParser(ABC):
    """Translates an external representation of a Mission into a MissionPlan."""

    @abstractmethod
    def parse(self, text: str) -> MissionPlan:
        """Raises MissionRejectedError when the text is malformed."""
