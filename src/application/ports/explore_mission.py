from abc import ABC, abstractmethod

from src.domain.mission_plan import MissionPlan


class ExploreMission(ABC):
    """Driving port: explore a Mission from its plan."""

    @abstractmethod
    def execute(self, plan: MissionPlan) -> None: ...
