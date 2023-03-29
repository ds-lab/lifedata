from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Iterable

from .annotator import Annotator
from .events import AssignedSampleRequested
from .events import EventDispatcher
from .events import NextSampleRequested
from .events import SampleAssigned
from .sample import Sample
from .sample_repository import SampleProjectRepository


class NoSampleAvailable(Exception):
    """
    Raised when no more samples are available for an annotator.
    """


@dataclass
class Assignment:
    annotator_id: str
    sample_id: str
    created: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class AssignmentRepository(ABC):
    """
    Manage the assignments of annotators to samples.
    """

    """Time until an assignment is no longer valid"""
    RELEASE_TIME = timedelta(hours=2)

    class NotFound(Exception):
        pass

    @abstractmethod
    def add(self, assignment: Assignment) -> None:
        """
        Assign the sample_id to the annotator
        """
        pass

    @abstractmethod
    def for_annotator(self, annotator: Annotator) -> Iterable[Assignment]:
        """
        Get all assignments for the given annotator.
        """
        pass

    @abstractmethod
    def query_for_relevant_sample_id(self, annotator: Annotator) -> dict:
        pass

    @abstractmethod
    def release_expired_assignments(self) -> None:
        """
        Releases in database assignments older than a given time
        """
        pass

    @abstractmethod
    def renew_assignment(self, assignment: Assignment) -> None:
        """
        Updates database assignment time on page reload
        """
        pass

    @abstractmethod
    def release_assignments(self, annotator_id: str) -> None:
        """
        Releases assignment in the database.
        """
        pass


class NoUnannotatedSamplesLeft(Exception):
    """
    All available samples have been annotated, i.e. we have reached full
    annotation coverage for the dataset.
    """

    pass


class TemporarilyNoSamplesLeft(Exception):
    """
    Indicates that currently no samples are left to be annotated (e.g. if new queryset needs to be created)
    """

    pass


class AssignmentService:
    def __init__(
        self,
        event_dispatcher: EventDispatcher,
        sample_repository: SampleProjectRepository,
        assignment_repository: AssignmentRepository,
    ):
        self._events = event_dispatcher
        self._assignments = assignment_repository
        self._samples = sample_repository

    def get_current_sample(self, annotator: Annotator) -> Sample:
        """
        Drops Assignments older than two hours
        Get the currently assigned sample for the given annotator, or assign
        a new one.
        """
        self._assignments.release_expired_assignments()

        assignments = list(self._assignments.for_annotator(annotator))
        if assignments:
            assignment = assignments[0]
            self._events.dispatch(
                AssignedSampleRequested(
                    annotator_id=annotator.id, sample_id=assignment.sample_id
                )
            )
            self._assignments.renew_assignment(assignment)
            return self._samples.by_id(assignment.sample_id)

        try:
            relevant_sample_params = self._assignments.query_for_relevant_sample_id(
                annotator
            )
            sample_id = relevant_sample_params["sample_id"]
            query_method = relevant_sample_params["query_method"]

            self._events.dispatch(
                NextSampleRequested(
                    query_method=query_method,
                    annotator_id=annotator.id,
                    sample_id=sample_id,
                )
            )
        except (TemporarilyNoSamplesLeft):

            # Re-raising valid exceptions.
            # raise e
            raise

        assignment = Assignment(
            sample_id=sample_id,  # type: ignore
            annotator_id=annotator.id,
        )
        self._assignments.add(assignment)
        self._events.dispatch(
            SampleAssigned(sample_id=sample_id, annotator_id=annotator.id)
        )
        return self._samples.by_id(sample_id)  # type: ignore
