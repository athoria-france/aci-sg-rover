from src.application.ports.explore_mission import ExploreMission
from src.application.ports.final_position_reporter import FinalPositionReporter
from src.application.ports.incident_reporter import IncidentReporter
from src.domain.mission import Mission
from src.domain.mission_plan import MissionPlan


class ExploreMissionUseCase(ExploreMission):
    def __init__(
        self, position_reporter: FinalPositionReporter, incident_reporter: IncidentReporter
    ) -> None:
        self._position_reporter = position_reporter
        self._incident_reporter = incident_reporter

    def execute(self, plan: MissionPlan) -> None:
        mission = Mission.from_plan(plan)
        mission.explore()
        self._incident_reporter.report(mission.pull_incidents())
        self._position_reporter.report(mission.final_positions())
