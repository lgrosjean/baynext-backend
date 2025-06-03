import logging

logger = logging.getLogger("uvicorn.error")


def get_logger(name: str):
    """
    Get a logger with the specified name.
    """
    return logger.getChild(name)
