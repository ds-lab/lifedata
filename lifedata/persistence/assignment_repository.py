from datetime import datetime
from datetime import timezone
from typing import Iterable

from loguru import logger

from . import models
from ..annotations.annotator import Annotator
from ..annotations.assignment import Assignment
from ..annotations.assignment import AssignmentRepository
from ..annotations.assignment import NoUnannotatedSamplesLeft
from ..persistence.queryset_db_repository import QuerySetDBRepository
from .database import Session
from .model_training_service import ModelTrainingService
from .model_training_service import RecreateQuerysetStatus


class DBAssignmentRepository(AssignmentRepository):
    """
    Managing the sample assignment information stored in
    the database.
    """

    def __init__(
        self,
        db: Session,
        queryset_db_repository: QuerySetDBRepository,
        model_training_service: ModelTrainingService,
    ):
        self._db = db
        self._queryset_db_repository = queryset_db_repository
        self._model_training_service = model_training_service

    def _instantiate(self, model: models.Assignment) -> Assignment:
        return Assignment(
            annotator_id=model.annotator_id,
            sample_id=model.sample_id,
            created=model.created,
        )

    def for_annotator(self, annotator: Annotator) -> Iterable[Assignment]:
        """
        Method to query for assigned sample for given Annotator

        Returns:
            Iterable[Assignment]: Iterable with Assignment objects for annotator queried from database
        """
        query = self._db.query(models.Assignment).filter_by(annotator_id=annotator.id)
        return (self._instantiate(a) for a in query.all())

    def query_for_relevant_sample_id(self, annotator: Annotator) -> dict:
        """
        Queries the most relevant and unassigned sample from the database and returns the sample_id.
        If no sample is found, a training is executed and a new queryset is created.

        Args:
            annotator (Annotator): Annotator object that describes the annotator who is to receive
            a sample.

        Returns:
            str: The sample_id of the sample to be displayed to the annotator.
        """

        query_method = "relevant"
        sample_id = self._queryset_db_repository.query_for_relevant_sample_id(annotator)

        if sample_id is None:
            # Execute ML iteration if configured in project instance lifedata_api.
            status = self._model_training_service.ml_update()

            if status == RecreateQuerysetStatus.NO_UNLABLED_SAMPLES:
                raise NoUnannotatedSamplesLeft()

            query_method = "random"
            sample_id = self._queryset_db_repository.query_random_sample(annotator)

        return {"sample_id": sample_id, "query_method": query_method}

    def add(self, assignment: Assignment) -> None:
        """
        Adds Assignment entry to database table
        """
        self._db.add(
            models.Assignment(
                annotator_id=assignment.annotator_id,
                sample_id=assignment.sample_id,
                created=assignment.created,
            )
        )

    def release_expired_assignments(self) -> None:
        """
        Clean all assignments older than RELEASE_TIME from Base class
        """
        drop_assignments_older_than = datetime.now(timezone.utc) - self.RELEASE_TIME
        outdated_assignments = self._db.query(models.Assignment).filter(
            models.Assignment.created < drop_assignments_older_than
        )
        assignments_to_drop = [self._instantiate(a) for a in outdated_assignments.all()]
        for assignment in assignments_to_drop:
            self.release_assignments(assignment.annotator_id)
        logger.debug(f"Dropped Assignments: {assignments_to_drop}")

    def renew_assignment(self, assignment: Assignment) -> None:
        """
        Renews created attribute for given Assignment
        """
        self._db.query(models.Assignment).filter_by(
            annotator_id=assignment.annotator_id, sample_id=assignment.sample_id
        ).update({"created": (assignment.created)})
        self._db.commit()

    def release_assignments(self, annotator_id: str) -> None:
        """
        Release Assignments from database to a given annotator_id

        Args:
            annotator_id (str): Database ID of a given annotator
        """
        self._db.query(models.Assignment).filter_by(annotator_id=annotator_id).delete()
