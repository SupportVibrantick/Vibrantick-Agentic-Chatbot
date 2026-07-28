from __future__ import annotations

import importlib
import inspect
import pkgutil
from types import ModuleType

from seeders.framework.base import BaseSeeder


class SeederDiscovery:
    """
    Automatically discovers every BaseSeeder subclass inside a package.
    """

    def discover(
        self,
        package_name: str,
    ) -> tuple[type[BaseSeeder], ...]:

        package = importlib.import_module(package_name)

        if not hasattr(package, "__path__"):
            raise ValueError(
                f"'{package_name}' is not a package."
            )

        discovered: list[type[BaseSeeder]] = []

        for _, module_name, _ in pkgutil.iter_modules(
            package.__path__
        ):
            module = importlib.import_module(
                f"{package_name}.{module_name}"
            )

            discovered.extend(
                self._find_seeders(module)
            )

        discovered.sort(
            key=lambda seeder: seeder.name
        )

        return tuple(discovered)

    def _find_seeders(
        self,
        module: ModuleType,
    ) -> list[type[BaseSeeder]]:

        seeders: list[type[BaseSeeder]] = []

        for _, obj in inspect.getmembers(
            module,
            inspect.isclass,
        ):

            if obj.__module__ != module.__name__:
                continue

            if (
                issubclass(obj, BaseSeeder)
                and obj is not BaseSeeder
                and not inspect.isabstract(obj)
            ):
                seeders.append(obj)

        return seeders