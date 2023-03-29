from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List
from typing import Optional

from ..annotations.annotation_count import AnnotationCount
from ..annotations.sample import Sample
from .consultation import Consultation
from .skip import Skip
from lifedata.annotations.annotator import Annotator


@dataclass
class Annotation:
    sample_id: str
    annotator_id: str
    labels: List[str]
    created: Optional[str]


class AnnotationRepository(ABC):
    @abstractmethod
    def annotate(self, annotation: Annotation) -> None:
        """
        Store the given annotation in the database. But doesn't release the
        assignment, that's done explicitly with ``release_assignments``
        """
        pass

    @abstractmethod
    def consult(self, annotation: Consultation) -> None:
        """
        Store the given annotation in the database and adds a consult request to annotationqueue.
        But doesn't release the assignment, that's done explicitly with ``release_assignments``
        """
        pass

    @abstractmethod
    def skip_sample(self, skip: Skip) -> None:
        """
        Store the given skip in the database. But doesn't release the
        assignment, that's done explicitly with ``release_assignments``
        """
        pass

    @abstractmethod
    def query_labeled(
        self,
        time_interval_start: Optional[datetime] = None,
        time_interval_stop: Optional[datetime] = None,
        annotator: Optional[str] = None,
    ) -> List[Annotation]:
        pass

    @abstractmethod
    def query_unlabeled(self) -> List[Sample]:
        pass

    @abstractmethod
    def query_skipped(self) -> List[Skip]:
        pass

    @abstractmethod
    def query_annotation_state_by_annotator(
        self, annotator: Annotator
    ) -> AnnotationCount:
        pass

    @abstractmethod
    def get_annotator_name_by_id(self, annotator_id: str) -> str:
        pass

    @abstractmethod
    def get_annotator_id_by_name(self, annotator_name: str) -> str:
        pass

    @abstractmethod
    def get_annotationqueue(self, annotator_id: str) -> List[Consultation]:
        pass
