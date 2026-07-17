from pathlib import Path

from loguru import logger

from .filters import context_filter
from .formatter import LOG_FORMAT

ROOT_LOG_DIR = Path("storage/logs")
ROOT_LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.remove()

# Console
logger.add(
    sink=lambda msg: print(msg, end=""),
    colorize=True,
    format=LOG_FORMAT,
)

LOG_CONFIG = {
    "admin": {
        "retention": "30 days",
    },
    "user": {
        "retention": "20 days",
    },
    "queue": {
        "retention": "15 days",
    },
}

for context, config in LOG_CONFIG.items():
    context_dir = ROOT_LOG_DIR / context
    context_dir.mkdir(parents=True, exist_ok=True)

    # INFO
    logger.add(
        context_dir / "info-{time:YYYY-MM-DD}.log",
        level="INFO",
        rotation="00:00",
        retention=config["retention"],
        compression="zip",
        filter=context_filter(context),
        format=LOG_FORMAT,
    )

    # ERROR
    logger.add(
        context_dir / "error-{time:YYYY-MM-DD}.log",
        level="ERROR",
        rotation="00:00",
        retention=config["retention"],
        compression="zip",
        filter=context_filter(context),
        format=LOG_FORMAT,
        backtrace=True,
        diagnose=True,
    )
