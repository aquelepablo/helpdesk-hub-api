import logging


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def getLogLevelNames() -> dict[str, int]:
    return logging.getLevelNamesMapping()
