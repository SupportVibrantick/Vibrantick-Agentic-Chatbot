from __future__ import annotations

from typing import Any, TypeVar, cast

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class ExecutionContext:
    """
    Shared runtime context for the entire seeding execution.

    Responsibilities
    ----------------
    - Provide a shared AsyncSession.
    - Share objects between seeders.
    - Store temporary runtime state.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self._data: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """Store a value in the execution context."""
        self._data[key] = value

    def get(
        self,
        key: str,
        default: T | None = None,
    ) -> T | Any:
        """
        Retrieve a value from the execution context.
        """
        return cast(T | Any, self._data.get(key, default))

    def has(self, key: str) -> bool:
        """Check whether a key exists."""
        return key in self._data

    def remove(self, key: str) -> None:
        """Remove a value if present."""
        self._data.pop(key, None)

    def clear(self) -> None:
        """Remove every stored value."""
        self._data.clear()

    def keys(self) -> list[str]:
        """Return all stored keys."""
        return list(self._data.keys())

    def values(self) -> list[Any]:
        """Return all stored values."""
        return list(self._data.values())

    def items(self):
        """Return key/value pairs."""
        return self._data.items()

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> None:
        self._data[key] = value

    @property
    def data(self) -> dict[str, Any]:
        """
        Read-only access to the internal storage.
        """
        return self._data