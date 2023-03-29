import logging

from loguru import logger

# Taken from
# https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup():
    """
    Make logging messages that are placed into the stdlib logging (like from
    other libraries, for example alembic) be passed through to loguru. This
    provides compatibility with these libraries and other loggings that might
    be used by users.
    """
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
