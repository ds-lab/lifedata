from functools import lru_cache
from typing import Callable
from typing import List
from typing import Optional

from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import status
from loguru import logger

from lifedata.annotations.annotation_count import AnnotationCount
from lifedata.annotations.annotation_service import AnnotationService
from lifedata.annotations.annotator import Annotator
from lifedata.annotations.assignment import AssignmentService
from lifedata.annotations.assignment import TemporarilyNoSamplesLeft
from lifedata.annotations.authentication import AuthenticationService
from lifedata.annotations.authentication import TokenDecoder
from lifedata.annotations.consultation import Consultation
from lifedata.annotations.events import EventDispatcher
from lifedata.annotations.sample import Sample
from lifedata.annotations.sample_repository import SampleProjectRepository
from lifedata.lifedata_api import LabelConfig
from lifedata.lifedata_api.load_lifedata_api import load_project_api
from lifedata.lifedata_api.load_lifedata_api import Project
from lifedata.persistence import DBAssignmentRepository
from lifedata.persistence import DBEventRepository
from lifedata.persistence import Session
from lifedata.persistence.annotation_db_repository import AnnotationsDBRepository
from lifedata.persistence.annotator_repository import AnnotatorDBRepository
from lifedata.persistence.model_training_service import ModelTrainingService
from lifedata.persistence.queryset_db_repository import QuerySetDBRepository
from lifedata.persistence.sample_db_repository import SampleDBRepository
from lifedata.webapi.no_auth_decoder import NoAuthDecoder
from lifedata.webapi.sample_widget import load_sample_display_data


def provide_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@lru_cache
def provide_project() -> Project:
    return load_project_api()


class InvalidAuthToken(Exception):
    pass


def provide_event_dispatcher(db: Session = Depends(provide_db)) -> EventDispatcher:
    return EventDispatcher(event_repository=DBEventRepository(db=db))


@lru_cache
def provide_auth_token_decoder(
    project: Project = Depends(provide_project),
) -> TokenDecoder:
    decoder = project.get_auth_token_decoder()
    if decoder is None:
        logger.warning(
            "No authentication backend was specified. This means all requests "
            "will be authenticated as a test user. To secure your setup, "
            "provide a ``get_auth_token_decoder`` function in your "
            "``lifedata_api.py``."
        )
        return NoAuthDecoder()

    return decoder


def provide_authentication_service(
    db: Session = Depends(provide_db),
    event_dispatcher: EventDispatcher = Depends(provide_event_dispatcher),
    token_decoder: TokenDecoder = Depends(provide_auth_token_decoder),
) -> AuthenticationService:
    return AuthenticationService(
        annotator_repository=AnnotatorDBRepository(
            db=db, event_dispatcher=event_dispatcher
        ),
        token_decoder=token_decoder,
    )


def provide_annotator(
    x_forwarded_access_token: Optional[str] = Header(None),
    auth: AuthenticationService = Depends(provide_authentication_service),
) -> Annotator:
    try:
        return auth.authenticate(x_forwarded_access_token or "")
    except Exception as exc:
        logger.exception(
            f"Invalid auth token (shouldn't happen behind oauth2-proxy): token={x_forwarded_access_token} exc={exc}"
        )
        raise HTTPException(status_code=400, detail="Invalid auth token")


def provide_queryset_db_repository(
    db: Session = Depends(provide_db),
) -> QuerySetDBRepository:
    return QuerySetDBRepository(db=db)


def provide_annotation_db_repository(
    db: Session = Depends(provide_db),
) -> AnnotationsDBRepository:
    return AnnotationsDBRepository(db=db)


def provide_sample_db_repository(
    db: Session = Depends(provide_db),
) -> SampleDBRepository:
    return SampleDBRepository(db=db)


def provide_label_metadata(project: Project = Depends(provide_project)) -> LabelConfig:
    return project.get_label_metadata()


def provide_queued_samples(
    annotator: Annotator = Depends(provide_annotator),
    annotation_db_repository: AnnotationsDBRepository = Depends(
        provide_annotation_db_repository
    ),
) -> List[Consultation]:
    return annotation_db_repository.get_annotationqueue(annotator.id)


def provide_model_training_service(
    project: Project = Depends(provide_project),
    annotation_db_repository: AnnotationsDBRepository = Depends(
        provide_annotation_db_repository
    ),
    queryset_db_repository: QuerySetDBRepository = Depends(
        provide_queryset_db_repository
    ),
) -> ModelTrainingService:
    return ModelTrainingService(
        project=project,
        annotation_repository=annotation_db_repository,
        queryset_repository=queryset_db_repository,
    )


def provide_domain_controller(
    db: Session = Depends(provide_db),
    event_dispatcher: EventDispatcher = Depends(provide_event_dispatcher),
    queryset_db_repository: QuerySetDBRepository = Depends(
        provide_queryset_db_repository
    ),
    model_training_service: ModelTrainingService = Depends(
        provide_model_training_service
    ),
) -> AnnotationService:

    return AnnotationService(
        event_dispatcher=event_dispatcher,
        queryset_repository=queryset_db_repository,
        assignment_repository=DBAssignmentRepository(
            db=db,
            queryset_db_repository=queryset_db_repository,
            model_training_service=model_training_service,
        ),
        annotation_repository=AnnotationsDBRepository(db=db),
    )


def provide_sample_repository(
    project: Project = Depends(provide_project),
) -> SampleProjectRepository:
    return SampleProjectRepository(project)


def provide_db_sample_state(
    sample_db_repository: SampleDBRepository = Depends(provide_sample_db_repository),
    annotation_repository: AnnotationsDBRepository = Depends(
        provide_annotation_db_repository
    ),
) -> status:
    # NOTE: This may not be the matching response codes but in this short time the best I could realize
    # Check if there are samples in the database
    db_samples = sample_db_repository.query_samples()
    if not db_samples:
        raise HTTPException(status_code=204, detail="No samples found in database")

    # Check if there are unannotated samples in the database
    unlabeled_db_samples = annotation_repository.query_unlabeled()
    if not unlabeled_db_samples:
        raise HTTPException(
            status_code=418, detail="No unlabeled samples found in database"
        )


def provide_annotation_count(
    annotator: Annotator = Depends(provide_annotator),
    annotation_db_repository: AnnotationsDBRepository = Depends(
        provide_annotation_db_repository
    ),
) -> AnnotationCount:
    annotation_count = annotation_db_repository.query_annotation_state_by_annotator(
        annotator
    )

    return annotation_count


def provide_sample(
    db: Session = Depends(provide_db),
    annotator: Annotator = Depends(provide_annotator),
    event_dispatcher: EventDispatcher = Depends(provide_event_dispatcher),
    sample_data_repository: SampleProjectRepository = Depends(
        provide_sample_repository
    ),
    queryset_db_repository: QuerySetDBRepository = Depends(
        provide_queryset_db_repository
    ),
    model_training_service: ModelTrainingService = Depends(
        provide_model_training_service
    ),
) -> Sample:
    assignment_service = AssignmentService(
        event_dispatcher=event_dispatcher,
        sample_repository=sample_data_repository,
        assignment_repository=DBAssignmentRepository(
            db=db,
            queryset_db_repository=queryset_db_repository,
            model_training_service=model_training_service,
        ),
    )

    try:
        sample = assignment_service.get_current_sample(annotator)
    except TemporarilyNoSamplesLeft as e:
        raise HTTPException(
            status_code=429,
            detail=str(e),
        )
    return sample


def provide_load_sample_display_data() -> Callable[[str], Optional[dict]]:
    """
    This will provide the with function that takes a ``sample_id`` and
    returns the according display data.
    """
    return load_sample_display_data
