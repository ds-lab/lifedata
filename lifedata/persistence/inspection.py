import time

import sqlalchemy
from loguru import logger
from sqlalchemy import text

from .database import get_engine


class TimeoutError(Exception):
    pass


def wait_for_database(timeout: float = 60, time_between_retries: float = 5) -> None:
    engine = get_engine()

    start = time.time()

    while True:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                return
        except sqlalchemy.exc.OperationalError as exc:
            logger.debug(
                f"Database not ready yet (error: {exc}). Waiting for startup ..."
            )
            remaining = timeout - (time.time() - start)
            if remaining <= 0:
                raise TimeoutError(
                    f"Database did not come up in time (timeout: {timeout}s)"
                )
            waiting_time = min(time_between_retries, remaining)
            time.sleep(waiting_time)


def is_initalized():
    engine = get_engine()
    inspector = sqlalchemy.inspect(engine)
    return len(inspector.get_table_names()) > 0
