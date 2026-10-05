from typing import assert_never

from src.domain.coordinates import Coordinates
from src.domain.incidents import LandingRejected, MissionIncident, MoveBlocked, Unavailability
from src.domain.instruction import Instruction
from src.domain.mission_plan import MissionPlan
from src.domain.plateau import Plateau
from src.domain.position import Position
from src.domain.rover import Rover, RoverId


class Mission:
    """Lands every Rover on the Plateau, then explores with each one in turn."""

    def __init__(self, plateau: Plateau) -> None:
        self._plateau = plateau
        self._rovers: list[Rover] = []
        self._incidents: list[MissionIncident] = []

    @staticmethod
    def from_plan(plan: MissionPlan) -> Mission:
        """Lands every Rover of the plan, each one identified by its order in the plan."""
        mission = Mission(plan.plateau)
        for order, rover_plan in enumerate(plan.rovers, start=1):
            mission.land(RoverId(order), rover_plan.initial_position, rover_plan.instructions)
        return mission

    def land(
        self, rover_id: RoverId, initial_position: Position, instructions: tuple[Instruction, ...]
    ) -> None:
        coordinates = initial_position.coordinates
        if not self._is_on_plateau(coordinates):
            self._incidents.append(
                LandingRejected(rover_id, initial_position, Unavailability.OUTSIDE_PLATEAU)
            )
        elif not self._is_free(coordinates):
            self._incidents.append(
                LandingRejected(rover_id, initial_position, Unavailability.OCCUPIED)
            )
        else:
            self._rovers.append(Rover(rover_id, initial_position, instructions))

    def explore(self) -> None:
        for rover in self._rovers:
            for instruction in rover.instructions:
                self._execute(rover, instruction)

    def final_positions(self) -> tuple[Position, ...]:
        return tuple(rover.position for rover in self._rovers)

    def pull_incidents(self) -> tuple[MissionIncident, ...]:
        incidents = tuple(self._incidents)
        self._incidents.clear()
        return incidents

    def _execute(self, rover: Rover, instruction: Instruction) -> None:
        match instruction:
            case Instruction.SPIN_LEFT:
                rover.spin_left()
            case Instruction.SPIN_RIGHT:
                rover.spin_right()
            case Instruction.MOVE:
                self._move(rover)
            case _:
                assert_never(instruction)

    def _move(self, rover: Rover) -> None:
        target = rover.next_coordinates()
        if not self._is_on_plateau(target):
            self._incidents.append(
                MoveBlocked(rover.id, rover.position, Unavailability.OUTSIDE_PLATEAU)
            )
        elif not self._is_free(target):
            self._incidents.append(MoveBlocked(rover.id, rover.position, Unavailability.OCCUPIED))
        else:
            rover.move_forward()

    def _is_on_plateau(self, coordinates: Coordinates) -> bool:
        return self._plateau.contains(coordinates)

    def _is_free(self, coordinates: Coordinates) -> bool:
        return all(rover.position.coordinates != coordinates for rover in self._rovers)
