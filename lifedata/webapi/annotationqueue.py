from typing import List

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from .providers import provide_project
from .providers import provide_queued_samples
from lifedata.lifedata_api import AnnotationQueue
from lifedata.lifedata_api import QueuedSample
from lifedata.lifedata_api.api import Project

router = APIRouter()


class AnnotationQueueConfig(BaseModel):
    annotation_queue_config: List


class QueuedSamples(BaseModel):
    queued_samples: List


def provide_annotation_queues_config(
    project: Project = Depends(provide_project),
) -> List[AnnotationQueue]:
    return project.get_annotation_queues_config()


@router.get("/annotationqueueconfig/", response_model=AnnotationQueueConfig)
def annotation_queues_config(
    annotation_queue_config: List[AnnotationQueue] = Depends(
        provide_annotation_queues_config
    ),
) -> AnnotationQueueConfig:
    """
    Combine the default submit button config and the submit button config defined in the project instance to use them in the UI
    """
    return AnnotationQueueConfig(annotation_queue_config=annotation_queue_config)


@router.get("/queuedsamples/", response_model=QueuedSamples)
def queued_samples(
    queued_samples: List[QueuedSample] = Depends(provide_queued_samples),
) -> QueuedSamples:
    """
    Routes API for relevant queued samples for an annotator
    """
    return QueuedSamples(queued_samples=queued_samples)
