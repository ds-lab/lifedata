from dataclasses import dataclass


@dataclass
class Consultation:
    sample_id: str
    queue_name: str
    requested_by: str
