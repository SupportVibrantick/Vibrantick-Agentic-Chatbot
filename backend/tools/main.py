import asyncio

from database.session import AsyncSessionLocal
from seeders.framework.manager import ExecutionManager
from seeders.framework.registry import SeederRegistry


async def main() -> int:

    registry = SeederRegistry()

    registry.discover(
        "backend.seeders.builders"
    )

    manager = ExecutionManager(
        session_factory=AsyncSessionLocal,
        registry=registry,
    )

    try:
        await manager.execute()
    except Exception as exc:
        print(f"\nSeeder execution failed:\n{exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(
        asyncio.run(main())
    )