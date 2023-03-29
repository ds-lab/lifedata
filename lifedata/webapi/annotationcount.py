from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status
from pydantic import BaseModel

from ..annotations.annotation_count import AnnotationCount
from .encoders import orjsonable_encoder
from .encoders import ORJSONNumpyResponse
from .providers import provide_annotation_count

router = APIRouter()


class AnnotationCountResponse(BaseModel):
    annotator_id: str
    overall: int
    monthly: int
    weekly: int


@router.get(
    "/count-by-annotator/",
    response_model=AnnotationCountResponse,
    response_class=ORJSONNumpyResponse,
)
def get_annotation_count(
    response: Response,
    label_count: AnnotationCount = Depends(provide_annotation_count),
) -> Optional[AnnotationCountResponse]:
    if not label_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return None
    return orjsonable_encoder(
        AnnotationCountResponse(
            annotator_id=label_count.annotator_id,
            overall=label_count.overall,
            monthly=label_count.monthly,
            weekly=label_count.weekly,
        )
    )
