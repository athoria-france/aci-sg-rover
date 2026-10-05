from abc import ABC, abstractmethod
from collections.abc import Sequence

from src.domain.position import Position


class FinalPositionReporter(ABC):
    """Driven port: publish the Final Position of each landed Rover, in landing order."""

    @abstractmethod
    def report(self, positions: Sequence[Position]) -> None: ...
