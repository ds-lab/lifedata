import os
import sys
from contextlib import contextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from . import annotationqueue
from . import auth
from . import label_config
from . import sample_view
from . import samples
from lifedata.annotations.sample_repository import SampleProjectRepository
from lifedata.logging import setup_logging
from lifedata.persistence.annotation_db_repository import AnnotationsDBRepository
from lifedata.persistence.inspection import is_initalized
from lifedata.persistence.inspection import wait_for_database
from lifedata.persistence.load_annotations import load_annotations
from lifedata.persistence.load_queryset import load_queryset_into_database
from lifedata.persistence.load_samples import load_samples_into_database
from lifedata.persistence.migrations.run_migrations import upgrade_to_head
from lifedata.persistence.queryset_db_repository import QuerySetDBRepository
from lifedata.persistence.sample_db_repository import SampleDBRepository
from lifedata.webapi import annotationcount
from lifedata.webapi import ui_strings
from lifedata.webapi.providers import provide_db
from lifedata.webapi.providers import provide_project

api = FastAPI()


# Configure allowed CORS origins with an environment variable. Multiple origins
# can be used, separated by spaces.
ALLOW_CORS_ORIGINS = os.environ.get("ALLOW_CORS_ORIGINS", "").split()

api.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[],
)

api.include_router(samples.router)
api.include_router(auth.router)
api.include_router(sample_view.router)
api.include_router(label_config.router)
api.include_router(annotationqueue.router)
api.include_router(ui_strings.router)
api.include_router(annotationcount.router)

api.mount(
    "/sampleview/component/static",
    sample_view.SampleViewFiles(),
    name="sampleview-component-static",
)

app = FastAPI()
app.mount("/api", api)


@app.on_event("startup")
def setup():
    setup_logging()

    try:
        wait_for_database()
    except TimeoutError:
        logger.error("No database available. Shutting down.")
        sys.exit(1)

    # If the database is not yet initialized, we do it right away.
    if not is_initalized():
        logger.info("Initializing database ...")
        upgrade_to_head()

        with contextmanager(provide_db)() as session:
            project = provide_project()
            sample_repository = SampleProjectRepository(project=project)
            sample_db_repository = SampleDBRepository(db=session)
            queryset_db_repository = QuerySetDBRepository(db=session)
            annotation_db_repository = AnnotationsDBRepository(db=session)

            load_samples_into_database(sample_repository, sample_db_repository)
            load_queryset_into_database(project, queryset_db_repository)
            load_annotations(project, annotation_db_repository)

            session.commit()
