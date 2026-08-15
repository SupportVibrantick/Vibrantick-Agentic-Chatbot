import asyncio
import traceback

from database.session import AsyncSessionLocal
from seeders.framework.manager import ExecutionManager
from seeders.framework.registry import SeederRegistry


async def main() -> int:

    registry = SeederRegistry()

    registry.discover("seeders")

    manager = ExecutionManager(
        session_factory=AsyncSessionLocal,
        registry=registry,
    )

    try:
        await manager.execute()

    except Exception as exc:
        print(f"\nSeeder execution failed:\n{exc}\n")
        traceback.print_exc()      # <-- ADD THIS
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(
        asyncio.run(main())
    )