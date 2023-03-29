from dataclasses import dataclass


@dataclass
class Skip:
    sample_id: str
    annotator_id: str
