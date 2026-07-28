from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class SeederExecutionResult:
    """
    Result of a single seeder execution.
    """

    name: str
    success: bool
    duration: float
    error: str | None = None


@dataclass(slots=True)
class ExecutionSummary:
    """
    Summary of an entire seeding execution.
    """

    started_at: datetime
    finished_at: datetime | None = None

    total_seeders: int = 0
    succeeded: int = 0
    failed: int = 0

    results: list[SeederExecutionResult] = field(
        default_factory=list
    )

    @property
    def successful(self) -> bool:
        """
        Returns True if every seeder completed successfully.
        """
        return self.failed == 0

    @property
    def duration(self) -> float | None:
        """
        Total execution time in seconds.
        """
        if self.finished_at is None:
            return None

        return (
            self.finished_at - self.started_at
        ).total_seconds()