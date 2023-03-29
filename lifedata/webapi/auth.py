from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from .providers import provide_annotator
from lifedata.annotations.annotator import Annotator

router = APIRouter()


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str


@router.get("/auth/", response_model=UserResponse)
def authenticate(
    annotator: Annotator = Depends(provide_annotator),
) -> UserResponse:
    """
    Retrieve annotator data for the logged in user.
    """
    bits = annotator.name.split(" ", maxsplit=1)
    if len(bits) == 1:
        first_name, last_name = bits[0], ""
    else:
        first_name, last_name = bits

    return UserResponse(
        id=annotator.id,
        first_name=first_name,
        last_name=last_name,
    )
