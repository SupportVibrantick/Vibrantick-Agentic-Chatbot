from __future__ import annotations

from typing import Iterator, Type

from tools.core.discovery import SeederDiscovery
from tools.seed.base import BaseSeeder


class SeederRegistry:
    """
    Registry for all seeders.
    """

    def __init__(self) -> None:
        self._seeders: dict[str, Type[BaseSeeder]] = {}

    def register(
        self,
        seeder: Type[BaseSeeder],
    ) -> None:
        """
        Register a seeder class.
        """
        if not seeder.name:
            raise ValueError(
                f"Seeder '{seeder.__name__}' must have a non-empty name."
            )

        if seeder.name in self._seeders:
            raise ValueError(
                f"Seeder '{seeder.name}' is already registered."
            )

        self._seeders[seeder.name] = seeder

    def discover(
        self,
        package: str,
    ) -> None:
        """
        Discover and register all seeders inside a package.
        """
        discovery = SeederDiscovery()

        for seeder in discovery.discover(package):
            self.register(seeder)

    def get(
        self,
        name: str,
    ) -> Type[BaseSeeder]:
        """
        Retrieve a registered seeder by name.
        """
        return self._seeders[name]

    def get_seeders(
        self,
    ) -> tuple[Type[BaseSeeder], ...]:
        """
        Return all registered seeders.
        """
        return tuple(self._seeders.values())

    def names(self) -> list[str]:
        """
        Return the names of all registered seeders.
        """
        return list(self._seeders.keys())

    def clear(self) -> None:
        """
        Remove all registered seeders.
        """
        self._seeders.clear()

    def __contains__(
        self,
        name: str,
    ) -> bool:
        return name in self._seeders

    def __len__(self) -> int:
        return len(self._seeders)

    def __iter__(
        self,
    ) -> Iterator[Type[BaseSeeder]]:
        return iter(self._seeders.values())