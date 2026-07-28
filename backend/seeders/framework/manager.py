from __future__ import annotations

import time
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from seeders.framework.context import ExecutionContext
from seeders.framework.dependency import DependencyResolver
from seeders.framework.registry import SeederRegistry
from seeders.framework.result import (
    ExecutionSummary,
    SeederExecutionResult,
)
from seeders.framework.scheduler import ExecutionScheduler


class ExecutionManager:
    """
    Executes all registered seeders inside a single database transaction.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        registry: SeederRegistry,
    ) -> None:
        self.session_factory = session_factory
        self.registry = registry

        self.resolver = DependencyResolver()
        self.scheduler = ExecutionScheduler()

        self.summary = ExecutionSummary(
            started_at=datetime.now()
        )

    async def execute(self) -> ExecutionSummary:
        """
        Execute every registered seeder.

        Returns
        -------
        ExecutionSummary
            Summary of the execution.
        """

        try:
            async with self.session_factory() as session:

                context = ExecutionContext(db=session)

                try:
                    await self._execute_seeders(context)
                    await session.commit()

                except Exception:
                    await session.rollback()
                    raise

        finally:
            self.summary.finished_at = datetime.now()

        self._print_summary()

        return self.summary

    async def _execute_seeders(
        self,
        context: ExecutionContext,
    ) -> None:
        """
        Execute all seeders according to the dependency graph.
        """

        plan = self.resolver.resolve(
            self.registry.get_seeders()
        )

        execution_levels = self.scheduler.schedule(plan)

        self.summary.total_seeders = plan.total_seeders

        for level in execution_levels:

            for seeder_class in level:

                seeder = seeder_class(context)

                start = time.perf_counter()

                try:
                    await seeder.before_run()
                    await seeder.run()
                    await seeder.after_run()

                    duration = time.perf_counter() - start

                    self.summary.results.append(
                        SeederExecutionResult(
                            name=seeder.name,
                            success=True,
                            duration=duration,
                        )
                    )

                    self.summary.succeeded += 1

                except Exception as exc:

                    duration = time.perf_counter() - start

                    self.summary.results.append(
                        SeederExecutionResult(
                            name=seeder.name,
                            success=False,
                            duration=duration,
                            error=str(exc),
                        )
                    )

                    self.summary.failed += 1

                    raise

    def _print_summary(self) -> None:
        """
        Print the execution summary.
        """

        print("\n========== Seeder Execution Summary ==========\n")

        for result in self.summary.results:

            status = "SUCCESS" if result.success else "FAILED"

            print(
                f"{status:<8}"
                f"{result.name:<30}"
                f"{result.duration:.2f}s"
            )

            if result.error:
                print(f"          Error: {result.error}")

        print("\n----------------------------------------------")
        print(f"Total Seeders : {self.summary.total_seeders}")
        print(f"Succeeded     : {self.summary.succeeded}")
        print(f"Failed        : {self.summary.failed}")

        if self.summary.finished_at:
            elapsed = (
                self.summary.finished_at
                - self.summary.started_at
            ).total_seconds()

            print(f"Total Time    : {elapsed:.2f}s")

        print("==============================================")