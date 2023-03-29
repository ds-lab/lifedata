from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterable
from typing import List
from typing import Optional

from .annotator import Annotator


@dataclass
class QueriedSample:
    sample_id: str
    query_index: int

    # TODO: Add more fields for data provenance, like querystrategy revision and shown
    # information.


class QuerySetRepository(ABC):
    @abstractmethod
    def query_random_sample(self, annotator: Annotator) -> str:
        """
        Query for a random sample
        """
        pass

    @abstractmethod
    def query_for_relevant_sample_id(self, annotator: Annotator) -> Optional[str]:
        """
        Queries the most relevant and unassigned sample returns the sample_id.
        """
        pass

    @abstractmethod
    def add_queryset(self, queryset: List[QueriedSample]) -> None:
        """
        Add samples to queryset
        """
        pass

    @abstractmethod
    def remove_queryset_sample(self, sample_id: str) -> None:
        """
        Remove sample from queryset
        """
        pass

    @abstractmethod
    def remove_queryset(self) -> None:
        """
        Remove queryset
        """
        pass

    @abstractmethod
    def query_queryset(self) -> Iterable[QueriedSample]:
        """
        Get actual queryset
        """
        pass
