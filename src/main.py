import sys

from src.adapters.cli import CommandLineInterface
from src.adapters.mission_text_parser import MissionTextParser
from src.adapters.stream_incident_reporter import StreamIncidentReporter
from src.adapters.stream_logger import StreamLogger
from src.adapters.stream_position_reporter import StreamPositionReporter
from src.application.use_cases.explore_mission import ExploreMissionUseCase


def main() -> int:
    """Composition Root: wires the adapters to the use case and runs the command line."""
    logger = StreamLogger(sys.stderr)
    explore_mission = ExploreMissionUseCase(
        StreamPositionReporter(sys.stdout), StreamIncidentReporter(logger)
    )
    cli = CommandLineInterface(logger, MissionTextParser(), explore_mission)
    return cli.run(sys.argv[1:])
