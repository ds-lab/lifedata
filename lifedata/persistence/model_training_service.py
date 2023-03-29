from enum import Enum
from threading import Thread

from loguru import logger

from lifedata.annotations.annotation import AnnotationRepository
from lifedata.annotations.queriedsample import QuerySetRepository
from lifedata.lifedata_api.load_lifedata_api import Project


class RecreateQuerysetStatus(Enum):
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    NO_UNLABLED_SAMPLES = "NO_UNLABLED_SAMPLES"


class ModelTrainingService:
    def __init__(
        self,
        project: Project,
        annotation_repository: AnnotationRepository,
        queryset_repository: QuerySetRepository,
    ):
        self._project = project
        self._annotation_repository = annotation_repository
        self._queryset_repository = queryset_repository

    def write_label_state(self) -> None:
        """
        Service to query database for unlabeled (Sample) and labeled (annotations) samples and write them out for project instance
        (e. g. as csv file)
        """
        unlabeled_samples = self._annotation_repository.query_unlabeled()
        labeled_samples = self._annotation_repository.query_labeled()
        skipped_samples = self._annotation_repository.query_skipped()

        self._project.write_label_state(
            labeled_samples, unlabeled_samples, skipped_samples
        )

    def add_queryset(self) -> None:
        """
        Service to read queryset (e. g. from csv file) result after training and add it to database.
        """
        queryset = self._project.get_queryset()

        self._queryset_repository.remove_queryset()

        self._queryset_repository.add_queryset(queryset)

    def ml_update(self) -> RecreateQuerysetStatus:
        """
        Service that updates the labelstate files underlying the ML pipeline, performs a training
        iteration of the network and writes the queryset created after the training to the database.

        Project instances `lifedata_api` (LIFEDATA Configuration) will return
        - True if a training is running
        - None if no training is in progress
        - True if a training should not be executed automatically after queryset is empty

        """
        unlabeled_samples = self._annotation_repository.query_unlabeled()
        if not unlabeled_samples:
            return RecreateQuerysetStatus.NO_UNLABLED_SAMPLES

        # This can be used at this point to throw an error and display the progress
        status = self._project.get_training_progress()
        if status:
            return RecreateQuerysetStatus.RUNNING

        self.write_label_state()

        def execute_training() -> None:
            logger.debug("A new queryset will be created")
            self._project.recreate_queryset()
            self.add_queryset()

        Thread(target=execute_training, daemon=True).start()

        return RecreateQuerysetStatus.STARTED
