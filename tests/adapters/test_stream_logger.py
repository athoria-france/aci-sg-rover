import io

import pytest

from src.adapters.stream_logger import Severity, StreamLogger


@pytest.mark.parametrize(
    ("severity", "expected"),
    [
        (Severity.ERROR, "[ERROR] something went wrong\n"),
        (Severity.WARNING, "[WARN] something went wrong\n"),
        (Severity.NONE, "something went wrong\n"),
    ],
)
def test_log_prefixes_message_with_severity(severity: Severity, expected: str) -> None:
    # Arrange
    stream = io.StringIO()
    logger = StreamLogger(stream)

    # Act
    logger.log(severity, "something went wrong")

    # Assert
    assert stream.getvalue() == expected
