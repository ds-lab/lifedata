from fastapi.encoders import jsonable_encoder
from loguru import logger

from . import models
from ..annotations.events import Event
from ..annotations.events import EventRepository
from .database import Session


class DBEventRepository(EventRepository):
    def __init__(self, db: Session):
        self._db = db

    def record(self, event: Event) -> None:
        payload = self._serialize_event(event)

        # Store event in database
        self._db.add(
            models.EventLog(
                name=event.event_name,
                recorded=event.recorded,
                payload=payload,
            )
        )
        self._db.commit()

        logger.info("dispatched {event}", event=payload)

    def _serialize_event(self, event: Event) -> dict:
        return {
            "event_name": event.event_name,
            "recorded": jsonable_encoder(event.recorded),
            "data": jsonable_encoder(event, exclude=["event_name", "recorded"]),
        }
