from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Sample:
    """
    Represents a sample that can be labelled
    """

    id: str


class SampleRepository(ABC):
    @abstractmethod
    def get_sample_ids(self):
        pass

    @abstractmethod
    def query_samples(self) -> List[Sample]:
        pass
