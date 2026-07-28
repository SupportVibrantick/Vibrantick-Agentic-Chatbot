from __future__ import annotations

from seeders.framework.base import BaseSeeder
from seeders.framework.plan import ExecutionPlan


class DependencyResolver:
    """
    Resolves the execution order of seeders using a dependency graph.
    """

    def resolve(
        self,
        seeders: tuple[type[BaseSeeder], ...],
    ) -> ExecutionPlan:

        available = set(seeders)

        graph: dict[
            type[BaseSeeder],
            list[type[BaseSeeder]],
        ] = {}

        resolved: list[type[BaseSeeder]] = []
        visited: set[type[BaseSeeder]] = set()
        visiting: set[type[BaseSeeder]] = set()

        def visit(seeder: type[BaseSeeder]) -> None:

            if seeder in visited:
                return

            if seeder not in available:
                raise RuntimeError(
                    f"Seeder '{seeder.__name__}' is required but not registered."
                )

            if seeder in visiting:
                raise RuntimeError(
                    f"Circular dependency detected involving '{seeder.__name__}'."
                )

            visiting.add(seeder)

            graph[seeder] = list(seeder.depends_on)

            for dependency in seeder.depends_on:
                visit(dependency)

            visiting.remove(seeder)
            visited.add(seeder)
            resolved.append(seeder)

        # Resolve dependency graph
        for seeder in seeders:
            visit(seeder)

        # Root seeders (no dependencies)
        roots = [
            seeder
            for seeder in seeders
            if not seeder.depends_on
        ]

        # Leaf seeders (nothing depends on them)
        dependencies: set[type[BaseSeeder]] = set()

        for seeder in seeders:
            dependencies.update(seeder.depends_on)

        leaves = [
            seeder
            for seeder in seeders
            if seeder not in dependencies
        ]

        execution_levels = self._build_execution_levels(resolved)

        return ExecutionPlan(
            ordered_seeders=tuple(resolved),
            dependency_graph=graph,
            root_seeders=tuple(roots),
            leaf_seeders=tuple(leaves),
            execution_levels=execution_levels,
        )

    def _build_execution_levels(
        self,
        resolved: list[type[BaseSeeder]],
    ) -> list[list[type[BaseSeeder]]]:
        """
        Group seeders into execution levels.

        All seeders in the same level have their dependencies
        satisfied by previous levels.
        """

        remaining = resolved.copy()
        completed: set[type[BaseSeeder]] = set()

        levels: list[list[type[BaseSeeder]]] = []

        while remaining:

            current_level = [
                seeder
                for seeder in remaining
                if all(
                    dependency in completed
                    for dependency in seeder.depends_on
                )
            ]

            if not current_level:
                raise RuntimeError(
                    "Unable to build execution levels."
                )

            levels.append(current_level)

            completed.update(current_level)

            remaining = [
                seeder
                for seeder in remaining
                if seeder not in current_level
            ]

        return levels