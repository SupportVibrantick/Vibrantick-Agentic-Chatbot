from .config import logger


def get_logger(context: str):
    return logger.bind(context=context)