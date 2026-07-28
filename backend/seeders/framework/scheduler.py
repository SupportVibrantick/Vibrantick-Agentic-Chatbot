from __future__ import annotations

from seeders.framework.base import BaseSeeder
from seeders.framework.plan import ExecutionPlan


class ExecutionScheduler:
    """
    Converts an ExecutionPlan into an executable schedule.

    Currently, the DependencyResolver already computes the
    execution levels, so the scheduler simply returns them.

    In the future this class can support:

    - Parallel execution
    - Batch execution
    - Priority scheduling
    - Conditional execution
    - Distributed execution
    """

    def schedule(
        self,
        plan: ExecutionPlan,
    ) -> list[list[type[BaseSeeder]]]:
        """
        Return the execution levels from the execution plan.
        """

        return plan.execution_levels