from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timezone
from typing import List

from pydantic import BaseModel
from pydantic import Field


class EventDispatcher:
    def __init__(self, event_repository: EventRepository):
        self._events = event_repository

    def dispatch(self, event: Event) -> None:
        self._events.record(event)
        # TODO: Implement mechanism to dispatch events to listeners.


class EventRepository(ABC):
    @abstractmethod
    def record(self, event: Event) -> None:
        """
        Persist the given event for later traceability.
        """
        pass


class Event(BaseModel):
    event_name: str

    recorded: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SampleAssigned(Event):
    event_name = "sample-assigned"

    annotator_id: str
    sample_id: str


class AssignedSampleRequested(Event):
    event_name = "assigned-sample-requested"

    annotator_id: str
    sample_id: str


class NextSampleRequested(Event):
    event_name = "next-sample-requested"

    query_method: str
    annotator_id: str
    sample_id: str


class SampleAnnotated(Event):
    event_name = "sample-annotated"

    annotator_id: str
    sample_id: str
    labels: List[str]


class ConsolutationRequested(Event):
    event_name = "consultation-requested"

    sample_id: str
    queue_name: str
    requested_by: str


class SampleSkipped(Event):
    event_name = "sample-skipped"

    sample_id: str
    annotator_id: str


class AssignmentCancelled(Event):
    """
    Triggered when an assignment is released without having a annotation
    created.
    """

    event_name = "assignment-cancelled"

    annotator_id: str
    sample_id: str


class AnnotatorCreated(Event):
    event_name = "annotator-created"

    annotator_id: str
