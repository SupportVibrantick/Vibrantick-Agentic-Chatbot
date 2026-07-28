from __future__ import annotations

from collections.abc import Iterator

from seeders.framework.base import BaseSeeder
from seeders.framework.discovery import SeederDiscovery


class SeederRegistry:
    """
    Registry responsible for discovering, registering,
    and providing access to all seeders.
    """

    def __init__(self) -> None:
        self._seeders: dict[str, type[BaseSeeder]] = {}

    def register(self, seeder: type[BaseSeeder]) -> None:
        """
        Register a seeder class.
        """

        if not seeder.name:
            raise ValueError(
                f"Seeder '{seeder.__name__}' must define a non-empty 'name'."
            )

        if seeder.name in self._seeders:
            raise ValueError(
                f"Seeder '{seeder.name}' is already registered."
            )

        self._seeders[seeder.name] = seeder

    def discover(self, package: str) -> None:
        """
        Automatically discover all seeders inside a package.
        """

        discovery = SeederDiscovery()

        for seeder in discovery.discover(package):
            self.register(seeder)

    def get(self, name: str) -> type[BaseSeeder]:
        """
        Get a seeder by name.
        """
        return self._seeders[name]

    def get_seeders(self) -> tuple[type[BaseSeeder], ...]:
        """
        Return all registered seeders.
        """
        return tuple(self._seeders.values())

    def names(self) -> list[str]:
        """
        Return all registered seeder names.
        """
        return list(self._seeders.keys())

    def clear(self) -> None:
        """
        Remove all registered seeders.
        """
        self._seeders.clear()

    def __contains__(self, name: str) -> bool:
        return name in self._seeders

    def __len__(self) -> int:
        return len(self._seeders)

    def __iter__(self) -> Iterator[type[BaseSeeder]]:
        return iter(self._seeders.values())