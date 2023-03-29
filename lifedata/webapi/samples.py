from typing import Callable
from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status
from pydantic import BaseModel

from .encoders import orjsonable_encoder
from .encoders import ORJSONNumpyResponse
from .providers import provide_annotator
from .providers import provide_db_sample_state
from .providers import provide_domain_controller
from .providers import provide_load_sample_display_data
from .providers import provide_sample
from lifedata.annotations.annotation import Annotation
from lifedata.annotations.annotation_service import AnnotationService
from lifedata.annotations.annotator import Annotator
from lifedata.annotations.consultation import Consultation
from lifedata.annotations.sample import Sample
from lifedata.annotations.skip import Skip
from lifedata.webapi.sample_widget import SampleDisplayData

router = APIRouter()


class SampleResponse(BaseModel):
    id: str
    data: SampleDisplayData


@router.get(
    "/samples/samplestate/",
    response_model=SampleResponse,
    response_class=ORJSONNumpyResponse,
)
def get_samplestate(sample_state=Depends(provide_db_sample_state)):
    return sample_state


@router.get(
    "/samples/by-id/{sample_id}/",
    response_model=SampleResponse,
    response_class=ORJSONNumpyResponse,
)
def get_sample_by_id(
    response: Response,
    sample_id: str,
    load_sample_display_data: Callable[[str], SampleDisplayData] = Depends(
        provide_load_sample_display_data
    ),
) -> Optional[SampleResponse]:
    if not sample_id:
        response.status_code = status.HTTP_204_NO_CONTENT
        return None

    return orjsonable_encoder(
        SampleResponse(id=sample_id, data=load_sample_display_data(sample_id))
    )


@router.get(
    "/samples/next/", response_model=SampleResponse, response_class=ORJSONNumpyResponse
)
def get_next_sample(
    response: Response,
    load_sample_display_data: Callable[[str], SampleDisplayData] = Depends(
        provide_load_sample_display_data
    ),
    sample: Optional[Sample] = Depends(provide_sample),
) -> Optional[SampleResponse]:
    if sample is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return None
    return orjsonable_encoder(
        SampleResponse(id=sample.id, data=load_sample_display_data(sample.id)),
    )


class AnnotationLabel(BaseModel):
    id: str
    name: str


class AnnotateRequest(BaseModel):
    labels: List[AnnotationLabel]


class ConsultRequest(BaseModel):
    labels: List[AnnotationLabel]
    queue_name: str


class AnnotateResponse(BaseModel):
    id: str


class ConsultResponse(BaseModel):
    id: str


class SkipResponse(BaseModel):
    id: str


# TODO: Needs testing.
@router.post(
    "/samples/annotate/{sample_id}/",
    response_model=AnnotateResponse,
    response_class=ORJSONNumpyResponse,
)
def annotate_sample(
    sample_id: str,
    body: AnnotateRequest,
    annotator: Annotator = Depends(provide_annotator),
    ctrl: AnnotationService = Depends(provide_domain_controller),
) -> AnnotateResponse:
    annotation = Annotation(
        annotator_id=annotator.id,
        sample_id=sample_id,
        labels=[label.id for label in body.labels],
        created=None,
    )

    ctrl.annotate_sample(annotation)

    return AnnotateResponse(id=sample_id)


# TODO: Needs testing.
@router.post(
    "/samples/consult/{sample_id}/",
    response_model=ConsultResponse,
    response_class=ORJSONNumpyResponse,
)
def consult_colleague(
    sample_id: str,
    body: ConsultRequest,
    annotator: Annotator = Depends(provide_annotator),
    ctrl: AnnotationService = Depends(provide_domain_controller),
) -> ConsultResponse:

    annotation = Annotation(
        annotator_id=annotator.id,
        sample_id=sample_id,
        labels=[label.id for label in body.labels],
        created=None,
    )
    consultation = Consultation(
        sample_id=sample_id,
        queue_name=body.queue_name,
        requested_by=annotator.id,
    )

    ctrl.consult_colleague(annotation, consultation)

    return ConsultResponse(id=sample_id)


# TODO: Needs testing.
@router.post(
    "/samples/skip/{sample_id}/",
    response_model=SkipResponse,
    response_class=ORJSONNumpyResponse,
)
def skip_sample(
    sample_id: str,
    annotator: Annotator = Depends(provide_annotator),
    ctrl: AnnotationService = Depends(provide_domain_controller),
) -> SkipResponse:
    skip = Skip(
        sample_id=sample_id,
        annotator_id=annotator.id,
    )

    ctrl.skip_sample(skip)

    return SkipResponse(id=sample_id)
