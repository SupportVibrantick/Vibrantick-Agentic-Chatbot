from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config


class AlembicManager:
    """
    Centralized Alembic manager for tests, development utilities,
    CI/CD and future automation.

    This class owns the Alembic configuration so the rest of the
    project never needs to deal with Config() directly.
    """

    def __init__(self) -> None:
        self._config = self._build_config()

    @staticmethod
    def _project_root() -> Path:
        """
        Return the project root directory.
        """
        return Path(__file__).resolve().parents[2]

    def _build_config(self) -> Config:
        """
        Create and configure the Alembic Config object.
        """
        return Config(str(self._project_root() / "alembic.ini"))

    @property
    def config(self) -> Config:
        """
        Expose the Alembic configuration if needed.
        """
        return self._config

    def upgrade(self, revision: str = "head") -> None:
        """
        Upgrade the database.
        """
        command.upgrade(self._config, revision)

    def downgrade(self, revision: str = "base") -> None:
        """
        Downgrade the database.
        """
        command.downgrade(self._config, revision)

    def stamp(self, revision: str = "head") -> None:
        """
        Stamp the database without executing migrations.
        """
        command.stamp(self._config, revision)

    def revision(
        self,
        message: str,
        autogenerate: bool = True,
    ) -> None:
        """
        Create a new Alembic revision.
        """
        command.revision(
            self._config,
            message=message,
            autogenerate=autogenerate,
        )

    def current(self, verbose: bool = False) -> None:
        """
        Show the current database revision.
        """
        command.current(
            self._config,
            verbose=verbose,
        )

    def history(self, verbose: bool = False) -> None:
        """
        Show migration history.
        """
        command.history(
            self._config,
            verbose=verbose,
        )

    def heads(self) -> None:
        """
        Show the current migration heads.
        """
        command.heads(self._config)

    def branches(self) -> None:
        """
        Show migration branches.
        """
        command.branches(self._config)

    def check(self) -> None:
        """
        Verify whether autogenerate would detect pending changes.
        Useful in CI pipelines.
        """
        command.check(self._config)


# Singleton used throughout the project.
alembic_manager = AlembicManager()