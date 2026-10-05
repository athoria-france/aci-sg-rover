from dataclasses import dataclass
from enum import Enum, auto

from src.domain.position import Position
from src.domain.rover import RoverId


class Unavailability(Enum):
    """Reasons why Coordinates cannot receive a Rover."""

    OUTSIDE_PLATEAU = auto()
    OCCUPIED = auto()


@dataclass(frozen=True)
class LandingRejected:
    rover_id: RoverId
    position: Position
    reason: Unavailability


@dataclass(frozen=True)
class MoveBlocked:
    rover_id: RoverId
    position: Position
    reason: Unavailability


type MissionIncident = LandingRejected | MoveBlocked
