from abc import ABC, abstractmethod
from collections.abc import Sequence

from src.domain.incidents import MissionIncident


class IncidentReporter(ABC):
    """Driven port: publish the Mission Incidents that occurred during the Mission."""

    @abstractmethod
    def report(self, incidents: Sequence[MissionIncident]) -> None: ...
