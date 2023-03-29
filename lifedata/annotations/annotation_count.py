from dataclasses import dataclass


@dataclass
class AnnotationCount:
    annotator_id: str
    overall: int
    monthly: int
    weekly: int
