from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from .providers import provide_project
from lifedata.lifedata_api import LabelConfig
from lifedata.lifedata_api.api import Project

router = APIRouter()


class LabelConfigResponse(BaseModel):
    labels: List[dict]
    label_type: str
    data_type: str


def provide_label_config(
    project: Project = Depends(provide_project),
) -> Optional[LabelConfig]:
    return project.get_label_metadata()


@router.get("/labels/", response_model=LabelConfigResponse)
def get_labels(
    label_metadata: LabelConfig = Depends(provide_label_config),
) -> LabelConfigResponse:
    """
    Use the Labels defined in Project instance to display them

    Args:
        label_metadata (LabelMetadata, optional): These are the label metadata defined in the project instance and obtained via providers. Defaults to Depends(provide_label_metadata).
    """

    return LabelConfigResponse(
        labels=label_metadata.labels,
        label_type=label_metadata.label_type,
        data_type=label_metadata.data_type,
    )
