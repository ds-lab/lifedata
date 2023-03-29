import json
from dataclasses import asdict
from typing import List

from lifedata.annotations.annotation import Annotation
from lifedata.annotations.sample import Sample
from lifedata.annotations.skip import Skip
from lifedata.persistence.annotation_db_repository import AnnotationsDBRepository


def create_labeled_json(
    labeled_samples: List[Annotation],
    unlabeled_samples: List[Sample],
    skipped_samples: List[Skip],
) -> str:
    labeled_dict = [asdict(sample) for sample in labeled_samples]
    unlabeled_dict = [asdict(sample) for sample in unlabeled_samples]
    skipped_dict = [asdict(sample) for sample in skipped_samples]

    labeled_state_dict = {
        "labeled": labeled_dict,
        "unlabeled": unlabeled_dict,
        "skipped": skipped_dict,
    }

    labeled_json = json.dumps(labeled_state_dict)

    return labeled_json


def query_labeled_state(annotations_db_repository: AnnotationsDBRepository) -> str:
    # Query database state
    labeled_samples = annotations_db_repository.query_labeled()
    unlabeled_samples = annotations_db_repository.query_unlabeled()
    skipped_samples = annotations_db_repository.query_skipped()

    return create_labeled_json(labeled_samples, unlabeled_samples, skipped_samples)
