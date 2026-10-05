from enum import Enum, auto
from typing import TextIO, assert_never


class Severity(Enum):
    """Severity of a logged message. NONE writes the message without any prefix."""

    ERROR = auto()
    WARNING = auto()
    NONE = auto()


class StreamLogger:
    """Writes each message on its own line, prefixed by its severity ('[ERROR] ...')."""

    def __init__(self, stream: TextIO) -> None:
        self._stream = stream

    def log(self, severity: Severity, message: str) -> None:
        self._stream.write(f"{self._format_prefix(severity)}{message}\n")

    @staticmethod
    def _format_prefix(severity: Severity) -> str:
        match severity:
            case Severity.ERROR:
                return "[ERROR] "
            case Severity.WARNING:
                return "[WARN] "
            case Severity.NONE:
                return ""
            case _:
                assert_never(severity)
