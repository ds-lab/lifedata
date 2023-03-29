import os

from loguru import logger

from . import stdlib_compat


def setup_logging():
    logfile = os.environ.get("LOGFILE")
    if not logfile:
        logger.info("No LOGFILE target configured. Only logging to stderr.")
        return
    logger.add(logfile)

    stdlib_compat.setup()
