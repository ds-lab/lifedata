from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from lifedata.annotations.events import AnnotatorCreated
from lifedata.annotations.events import EventDispatcher


@dataclass
class Annotator:
    """
    Represents a single user who label given samples.
    """

    id: str
    name: str
    email: str
    formal_training: List[str]


@dataclass
class UserInfo:
    """
    This is the minimal info that must be given by an external authentication
    provider.  It will be used to check for an existing annotator or create
    one based on this data.
    """

    id: str
    email: str
    name: str


class AnnotatorRepository(ABC):
    class NotFound(Exception):
        pass

    def __init__(
        self,
        event_dispatcher: EventDispatcher,
    ):
        self._events = event_dispatcher

    @abstractmethod
    def by_id(self, id: str) -> Annotator:
        pass

    @abstractmethod
    def create(self, info: UserInfo) -> Annotator:
        pass

    def get_or_create(self, info: UserInfo) -> Annotator:
        try:
            return self.by_id(info.id)
        except self.NotFound:
            annotator = self.create(info)
            self._events.dispatch(AnnotatorCreated(annotator_id=annotator.id))
            return annotator
