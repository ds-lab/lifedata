from loguru import logger

from lifedata.annotations.annotation import AnnotationRepository
from lifedata.lifedata_api.load_lifedata_api import Project


def load_annotations(
    project: Project, annotation_repository: AnnotationRepository
) -> None:
    """
    Load annotations provided by the projects state (e.g. via data trcked by dvc).

    This is usually only ever required if you are providing an initial set of annotations that you would like to maintain in the lifedata database.
    """
    logger.info("Loading initial annotations ...")

    loaded = 0
    for annotation in project.get_labeled_state():
        annotation_repository.annotate(annotation)
        loaded += 1

    logger.info(f"Loaded {loaded} annotations")
