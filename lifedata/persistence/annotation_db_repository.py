from datetime import datetime
from typing import List
from typing import Optional

import sqlalchemy
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.functions import now

from ..annotations.annotation import Annotation
from ..annotations.annotation import AnnotationRepository
from ..annotations.annotation_count import AnnotationCount
from ..annotations.consultation import Consultation
from ..annotations.sample import Sample
from ..annotations.skip import Skip
from ..persistence import models
from ..persistence.database import Session
from lifedata.annotations.annotator import Annotator


class AnnotationsDBRepository(AnnotationRepository):
    def __init__(self, db: Session):
        self._db = db

    def _instantiate_sample(self, model: models.Sample) -> Sample:
        return Sample(id=model.id)  # type: ignore

    def _instantiate_annotation(self, model: models.Annotation) -> Annotation:
        return Annotation(
            sample_id=model.sample_id,
            annotator_id=model.annotator_id,
            labels=model.labels,
            created=model.created.strftime("%m/%d/%Y, %H:%M:%S"),
        )

    def _instantiate_skip(self, model: models.Skipped) -> Skip:
        return Skip(sample_id=model.sample_id, annotator_id=model.annotator_id)

    def _instantiate_queue(self, model: models.AnnotationQueue) -> Consultation:
        # This is a method to format outputs for api endpoint
        return Consultation(
            sample_id=model.AnnotationQueue.sample_id,
            queue_name=model.AnnotationQueue.queue_name,
            requested_by=model.AnnotationQueue.requested_by,
        )

    def annotate(self, annotation: Annotation) -> None:
        """
        Executes an upsert for the annotations table.

        First an `insert into` is tried. If the combination of
        `sample_id` and `annotator_id` already exists, the constraint condition
        `sample_id_annotator_id_unique` is violated and an update of the sample is executed instead.

        The matching SQL query is:

        INSERT INTO annotations (sample_id, annotator_id, labels)
        VALUES ('<sample_id>', '<annotator_id>', '<labels>')
        ON CONFLICT ON CONSTRAINT sample_id_annotator_id_unique
        DO UPDATE SET sample_id='<sample_id>', annotator_id='<annotator_id>', labels='<label>', created=now();
        """
        self._db.execute(
            insert(models.Annotation)
            .values(
                sample_id=annotation.sample_id,
                annotator_id=annotation.annotator_id,
                labels=annotation.labels,
            )
            .on_conflict_do_update(
                constraint="sample_id_annotator_id_unique",
                set_=dict(
                    sample_id=annotation.sample_id,
                    annotator_id=annotation.annotator_id,
                    labels=annotation.labels,
                    # The date used is based on the server time, as in log entries or annotations.
                    created=now(),
                ),
            )
        )
        self._db.commit()

    def consult(self, consultation: Consultation) -> None:
        """
        Store the given consultation request in the database.

        Executes an upsert for the annotationqueue table.

        First an `insert into` is tried. If the combination of
        `sample_id` and `requested_by` already exists, the constraint condition
        `sample_id_requested_id_unique` is violated and an update of the sample is executed instead.
        """
        self._db.execute(
            insert(models.AnnotationQueue)
            .values(
                sample_id=consultation.sample_id,
                queue_name=consultation.queue_name,
                requested_by=consultation.requested_by,
            )
            .on_conflict_do_update(
                constraint="sample_id_requested_by_unique",
                set_=dict(
                    sample_id=consultation.sample_id,
                    queue_name=consultation.queue_name,
                    requested_by=consultation.requested_by,
                    # The date used is based on the server time, as in log entries or annotations.
                    created=now(),
                ),
            )
        )
        self._db.commit()

    def skip_sample(self, skip: Skip) -> None:
        """
        Store the given skip in the database.
        """
        self._db.add(
            models.Skipped(
                sample_id=skip.sample_id,
                annotator_id=skip.annotator_id,
            )
        )
        self._db.commit()

    def query_labeled(
        self,
        time_interval_start: Optional[datetime] = None,
        time_interval_stop: Optional[datetime] = None,
        annotator: Optional[str] = None,
    ) -> List[Annotation]:
        """
        Queries all labeled samples from the database including their labels. Filters for time interval and for special annotator can be used.

        Returns:
            List[Annotation]: List of labelled samples from the database including their labels and creation date
        """
        annotated_samples = self._db.query(models.Annotation).filter(
            models.Annotation.sample_id is not None
        )

        if time_interval_start:
            annotated_samples = annotated_samples.filter(
                models.Annotation.created >= time_interval_start
            )
        if time_interval_stop:
            annotated_samples = annotated_samples.filter(
                models.Annotation.created <= time_interval_stop
            )

        if annotator:
            annotated_samples = annotated_samples.filter(
                models.Annotation.annotator_id == annotator
            )

        return [self._instantiate_annotation(a) for a in annotated_samples.all()]

    def query_unlabeled(self) -> List[Sample]:
        """
        Queries all unlabeled samples from the database

        Returns:
            List[Sample]: List of unlabeled samples from the database
        """
        unlabeled_samples = (
            self._db.query(models.Sample)
            .outerjoin(
                models.Annotation,
                models.Sample.id == models.Annotation.sample_id,
            )
            .filter(models.Annotation.sample_id.is_(None))
        )

        return [self._instantiate_sample(a) for a in unlabeled_samples.all()]

    def query_skipped(self) -> List[Skip]:
        """
        Queries all skipped samples from the database including their annotator
        """
        return [self._instantiate_skip(a) for a in self._db.query(models.Skipped).all()]

    def query_annotation_state_by_annotator(
        self, annotator: Annotator
    ) -> AnnotationCount:
        """
        Queries how many samples a specific annotator has annotated in total, monthly and weekly
        """
        query_overall_count = text(
            f"SELECT COUNT(*) FROM annotations WHERE annotator_id='{annotator.id}';"
        )
        query_monthly_count = text(
            f"SELECT COUNT(*) FROM annotations WHERE annotator_id='{annotator.id}' AND "
            f"EXTRACT(MONTH from created) = EXTRACT(MONTH from current_date) AND "
            f"EXTRACT(YEAR from created) = EXTRACT(YEAR from current_date);"
        )
        query_weekly_count = text(
            f"SELECT COUNT(*) FROM annotations WHERE annotator_id='{annotator.id}' AND created > current_date - 7;"
        )

        overall_count = self._db.execute(query_overall_count)
        monthly_count = self._db.execute(query_monthly_count)
        weekly_count = self._db.execute(query_weekly_count)

        return AnnotationCount(
            annotator_id=annotator.id,
            overall=overall_count.first()[0],
            monthly=monthly_count.first()[0],
            weekly=weekly_count.first()[0],
        )

    def query_annotation_report(
        self,
        interval_start_date: Optional[datetime],
        interval_stop_date: Optional[datetime],
    ) -> List[sqlalchemy.engine.row.Row]:
        """
        Queries an annotations report which shows how many samples each annotator has annotated in
        total, monthly, weekly and optionally in a time interval.
        """
        if interval_start_date or interval_stop_date:
            select_statement = "SELECT q1.*, \
               q2.past_7_days, \
               q3.current_month, \
               q4.time_interval"
            if interval_start_date and interval_stop_date:
                filter_statement = f"full outer join (SELECT b.name, \
                            a.annotator_id, \
                            Count(*) AS time_interval \
                    FROM   annotations a \
                            inner join annotators b \
                                    ON a.annotator_id = b.id \
                    WHERE  created > '{interval_start_date}' \
                        AND created < '{interval_stop_date}' \
                    GROUP  BY b.name, \
                                a.annotator_id) AS q4 \
                ON q1.annotator_id = q4.annotator_id;"
            elif interval_start_date:
                filter_statement = f"full outer join (SELECT b.name, \
                            a.annotator_id, \
                            Count(*) AS time_interval \
                    FROM   annotations a \
                            inner join annotators b \
                                    ON a.annotator_id = b.id \
                    WHERE  created > '{interval_start_date}' \
                    GROUP  BY b.name, \
                                a.annotator_id) AS q4 \
                ON q1.annotator_id = q4.annotator_id;"
            elif interval_stop_date:
                filter_statement = f"full outer join (SELECT b.name, \
                            a.annotator_id, \
                            Count(*) AS time_interval \
                    FROM   annotations a \
                            inner join annotators b \
                                    ON a.annotator_id = b.id \
                        AND created < '{interval_stop_date}' \
                    GROUP  BY b.name, \
                                a.annotator_id) AS q4 \
                ON q1.annotator_id = q4.annotator_id;"
        else:
            select_statement = "SELECT q1.*, \
               q2.past_7_days, \
               q3.current_month"
            filter_statement = ";"

        query_expression = f"{select_statement} \
        FROM   (SELECT b.name, \
                       b.email,\
                       a.annotator_id, \
                       Count(*) AS count_ALL \
                FROM   annotations a \
                       inner join annotators b \
                               ON a.annotator_id = b.id \
                GROUP  BY b.name, \
                          b.email, \
                          a.annotator_id) AS q1 \
               full outer join (SELECT b.name, \
                                       a.annotator_id, \
                                       Count(*) AS past_7_days \
                                FROM   annotations a \
                                       inner join annotators b \
                                               ON a.annotator_id = b.id \
                                WHERE  created > current_date - 7 \
                                GROUP  BY b.name, \
                                          a.annotator_id) AS q2 \
                            ON q1.annotator_id = q2.annotator_id \
               full outer join (SELECT b.name, \
                                       a.annotator_id, \
                                       Count(*) AS current_month \
                                FROM   annotations a \
                                       inner join annotators b \
                                               ON a.annotator_id = b.id \
                                WHERE  EXTRACT(MONTH from created) = EXTRACT(MONTH from current_date) \
                                GROUP  BY b.name, \
                                          a.annotator_id) AS q3 \
                            ON q1.annotator_id = q3.annotator_id {filter_statement}"

        annotation_report = self._db.execute(query_expression)

        return annotation_report.all()

    def get_annotator_name_by_id(self, annotator_id: str) -> str:
        annotator_name_queried = self._db.query(models.Annotator).filter(
            models.Annotator.id == annotator_id
        )
        return annotator_name_queried.all()[0].name

    def get_annotator_id_by_name(self, annotator_name: str) -> str:
        annotator_id_queried = self._db.query(models.Annotator).filter(
            models.Annotator.name == annotator_name
        )
        return annotator_id_queried.first().id

    def get_annotationqueue(self, annotator_id: str) -> List[Consultation]:
        """
         Select which samples should be displayed to the actual annotator for a second optinion

        For SQL-query we have a few steps:
         - Query samples from queriedsamples that were not requested by the actual user
         - Query annotator skipped samples
         - Query already annotated samples
         - Find all samples that are not queried or skipped by the actual user and also do not have a solution
        """
        # Query samples from queriedsamples that were not requested by the user
        # SELECT * FROM annotationqueue WHERE sample_id NOT IN (SELECT sample_id FROM annotationqueue WHERE requested_by={annotator_id})
        not_annotator_queued = self._db.query(models.AnnotationQueue).filter(
            models.AnnotationQueue.sample_id.not_in(
                self._db.query(models.AnnotationQueue.sample_id).filter(
                    models.AnnotationQueue.requested_by == annotator_id
                )
            )
        )

        # Query skipped samples by annotator
        # SELECT * FROM skippedsamples WHERE annotator_id=={annotator_id})
        annotator_skipped_samples = self._db.query(models.Skipped.sample_id).filter(
            models.Skipped.annotator_id == annotator_id
        )

        # Query already annotated samples
        # SELECT annotationqueuescount.sample_id FROM (SELECT sample_id, COUNT(sample_id) FROM annotationqueue GROUP BY sample_id) AS annotationqueuescount JOIN (SELECT sample_id, COUNT(sample_id) FROM annotations GROUP BY sample_id) AS annotationscount ON annotationqueuescount.sample_id=annotationscount.sample_id WHERE annotationqueuescount.count < annotationscount.count)
        annotationqueuescounter = (
            self._db.query(
                models.AnnotationQueue.sample_id,
                func.count(models.AnnotationQueue.sample_id).label(
                    "annotationqueuescount"
                ),
            )
            .group_by(models.AnnotationQueue.sample_id)
            .subquery("annotationqueuescounter")
        )
        annotationscounter = (
            self._db.query(
                models.Annotation.sample_id,
                func.count(models.Annotation.sample_id).label("annotationcount"),
            )
            .group_by(models.Annotation.sample_id)
            .subquery("annotationscounter")
        )
        joined_table = (
            select(annotationqueuescounter.c.sample_id)
            .select_from(
                annotationqueuescounter.join(
                    annotationscounter,
                    annotationqueuescounter.c.sample_id
                    == annotationscounter.c.sample_id,
                )
            )
            .filter(
                annotationqueuescounter.c.annotationqueuescount
                < annotationscounter.c.annotationcount
            )
        )

        # Combine filter
        queued_samples = self._db.execute(
            not_annotator_queued.filter(
                models.AnnotationQueue.sample_id.not_in(joined_table)
            ).filter(models.AnnotationQueue.sample_id.not_in(annotator_skipped_samples))
        )
        return [self._instantiate_queue(a) for a in queued_samples.all()]
