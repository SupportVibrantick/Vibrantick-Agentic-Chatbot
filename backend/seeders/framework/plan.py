from __future__ import annotations

from dataclasses import dataclass, field

from seeders.framework.base import BaseSeeder


@dataclass(slots=True)
class ExecutionPlan:
    """
    Represents the resolved execution plan produced by the
    DependencyResolver.

    This plan is consumed by the ExecutionScheduler and
    ExecutionManager.
    """

    ordered_seeders: tuple[type[BaseSeeder], ...]

    dependency_graph: dict[
        type[BaseSeeder],
        list[type[BaseSeeder]],
    ] = field(default_factory=dict)

    root_seeders: tuple[type[BaseSeeder], ...] = ()

    leaf_seeders: tuple[type[BaseSeeder], ...] = ()

    execution_levels: list[
        list[type[BaseSeeder]]
    ] = field(default_factory=list)

    @property
    def total_seeders(self) -> int:
        """
        Total number of seeders in the execution plan.
        """
        return len(self.ordered_seeders)