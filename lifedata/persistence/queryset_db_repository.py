from typing import Iterable
from typing import List
from typing import Optional

from loguru import logger
from sqlalchemy.sql.expression import func

from ..annotations.annotator import Annotator
from ..annotations.queriedsample import QueriedSample
from ..annotations.queriedsample import QuerySetRepository
from ..persistence import models
from ..persistence.database import Session


class QuerySetDBRepository(QuerySetRepository):
    def __init__(self, db: Session):
        self._db = db

    def _instantiate(self, model: models.QueriedSample) -> QueriedSample:
        """
        Convert database objects to local objects
        """
        return QueriedSample(
            sample_id=model.sample_id,
            query_index=model.query_index,
        )

    def query_random_sample(self, annotator: Annotator) -> str:  # type: ignore
        """
        If training runs already this method is called to query for a random unlabeled and unassigned sample
        """

        queried_sample = (
            (
                self._db.query(models.Sample)
                .outerjoin(
                    models.Annotation,
                    models.Sample.id == models.Annotation.sample_id,
                )
                .filter(models.Annotation.labels.is_(None))
                .outerjoin(
                    models.Assignment,
                    models.Sample.id == models.Assignment.sample_id,
                )
                .filter(models.Assignment.sample_id.is_(None))
            )
            .filter(models.Assignment.sample_id.is_(None))
            .order_by(func.random())
        )

        return queried_sample.first().id

    def query_for_relevant_sample_id(self, annotator: Annotator) -> Optional[str]:  # type: ignore
        """
        NOTE: If you sometimes want to select samples to resubmit to an annotator, this is the place to implement it.

        Queries the most relevant and unassigned sample from the database and returns the sample_id.
        If no sample is found, a training is executed and a new queryset is created.

        Args:
            annotator (Annotator): Annotator object that describes the annotator who is to receive
            a sample.

        Returns:
            str: The sample_id of the sample to be displayed to the annotator.
        """
        # NOTE: This query must be removed if we want to use overannotations.
        # After removal, it must be ensured that no unintentional sample is
        # overannotated (queryset.csv must not change state in db).
        annotated_samples = self._db.query(models.Annotation.sample_id)

        assigned_samples = self._db.query(models.Assignment.sample_id)
        annotator_skipped_samples = self._db.query(models.Skipped.sample_id).filter(
            models.Skipped.annotator_id == annotator.id
        )

        # NOTE: The following query ensures that the next displayed sample:
        # - Is in the queryset
        # - Is actual not assigned
        # - Is not skipped by the actual annotator
        # - Is actually not annotated
        queried_sample = (
            self._db.query(models.QueriedSample.sample_id)
            .filter(models.QueriedSample.sample_id.not_in(assigned_samples))
            .filter(models.QueriedSample.sample_id.not_in(annotator_skipped_samples))
            .filter(models.QueriedSample.sample_id.not_in(annotated_samples))
            .order_by(models.QueriedSample.query_index)
        )

        if queried_sample.first():
            return queried_sample.first().sample_id

    def add_queryset(self, queryset: List[QueriedSample]) -> None:
        """
        Add samples to `queriedsamples`
        """
        for queriedsample in queryset:
            self._db.add(
                models.QueriedSample(
                    sample_id=queriedsample.sample_id,
                    query_index=queriedsample.query_index,
                )
            )
            self._db.commit()

            logger.info(
                "New queried sample instance {instance} created", instance=queriedsample
            )

    def remove_queryset_sample(self, sample_id: str) -> None:
        """
        Remove entry from `queriedsamples`
        """
        self._db.query(models.QueriedSample).filter(
            models.QueriedSample.sample_id == sample_id
        ).delete()
        self._db.commit()
        logger.info(
            f"Queryset sample - {sample_id} removed from queryset table in database"
        )

    def remove_queryset(self) -> None:
        """
        Remove all entries from `queriedsamples`
        """
        self._db.query(models.QueriedSample).delete()
        logger.info("Queryset removed from database")
        self._db.commit()

    def query_queryset(self) -> Iterable[QueriedSample]:
        """
        Querys for `queriedsamples` table in the database
        """
        queryset = self._db.query(models.QueriedSample)
        return (self._instantiate(a) for a in queryset.all())
