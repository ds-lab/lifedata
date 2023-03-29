from .annotation import Annotation
from .annotation import AnnotationRepository
from .assignment import AssignmentRepository
from .consultation import Consultation
from .events import ConsolutationRequested
from .events import EventDispatcher
from .events import SampleAnnotated
from .events import SampleSkipped
from .queriedsample import QuerySetRepository
from .skip import Skip


class AnnotationService:
    def __init__(
        self,
        event_dispatcher: EventDispatcher,
        queryset_repository: QuerySetRepository,
        assignment_repository: AssignmentRepository,
        annotation_repository: AnnotationRepository,
    ):
        self._events = event_dispatcher
        self._queryset_repository = queryset_repository
        self._assignments = assignment_repository
        self._annotation_repository = annotation_repository

    def annotate_sample(self, annotation: Annotation) -> None:
        """
        Adds annotation entry and removes assignment entry for sample from database
        """
        self._annotation_repository.annotate(annotation)
        self._assignments.release_assignments(annotator_id=annotation.annotator_id)

        self._events.dispatch(
            SampleAnnotated(
                annotator_id=annotation.annotator_id,
                sample_id=annotation.sample_id,
                labels=annotation.labels,
            )
        )

        self._queryset_repository.remove_queryset_sample(annotation.sample_id)

    def consult_colleague(
        self, annotation: Annotation, consultation: Consultation
    ) -> None:
        self.annotate_sample(annotation)

        self._annotation_repository.consult(consultation)
        self._events.dispatch(
            ConsolutationRequested(
                sample_id=consultation.sample_id,
                queue_name=consultation.queue_name,
                requested_by=consultation.requested_by,
            )
        )

    def skip_sample(self, skip: Skip) -> None:
        """
        Adds skip entry and removes assignment entry for sample in database
        """
        self._annotation_repository.skip_sample(skip)
        self._assignments.release_assignments(annotator_id=skip.annotator_id)

        self._events.dispatch(
            SampleSkipped(
                sample_id=skip.sample_id,
                annotator_id=skip.annotator_id,
            )
        )
