from dataclasses import dataclass

from src.domain.instruction import Instruction
from src.domain.plateau import Plateau
from src.domain.position import Position


@dataclass(frozen=True)
class RoverPlan:
    """What a Rover needs to land and explore: its initial Position and its Instructions."""

    initial_position: Position
    instructions: tuple[Instruction, ...]


@dataclass(frozen=True)
class MissionPlan:
    """What a Mission needs to start: the Plateau and, in landing order, each RoverPlan."""

    plateau: Plateau
    rovers: tuple[RoverPlan, ...]
