import os
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from pydantic import BaseModel
from starlette.staticfiles import PathLike
from starlette.staticfiles import Response
from starlette.staticfiles import Scope
from starlette.staticfiles import StaticFiles

from .providers import provide_project
from lifedata.lifedata_api.api import Project
from lifedata.lifedata_api.sample_view import SampleView

router = APIRouter()


class SampleViewFiles(StaticFiles):
    """
    This class slightly modifies the behaviour of StaticFiles. This is
    necessary since StaticFiles needs to know about the configured directory
    to serve during instantiation.
    We however want to lazy-load the lifedata_api which configures the
    SampleView, which points us to the correct directory to serve. Therefore
    we move this logic to ``check_config`` that is executed during the first
    request to the endpoint.
    """

    # Implicitly requires `aiofiles` package.

    def __init__(self) -> None:
        self.directory: Optional[str] = None
        self.packages = None
        self.all_directories: List[str] = []
        self.html = True
        self.config_checked = False

    def lookup_path(self, path: PathLike) -> Tuple[str, Any]:  # type: ignore
        # Follow symlink
        for directory in self.all_directories:

            full_path = os.path.realpath(os.path.join(directory, path))

            try:
                stat_result = os.stat(full_path)
                return (full_path, stat_result)
            except FileNotFoundError:
                pass
                return ("", None)

    async def check_config(self) -> None:
        # The configuration is only checked on first request. We take that
        # chance to late-initialize the StaticFiles mount point.
        from lifedata.lifedata_api.load_lifedata_api import load_project_api

        project = load_project_api()

        self.sample_view = project.get_sample_view()

        if self.sample_view is not None and self.sample_view.directory is not None:
            self.directory = str(self.sample_view.directory)
            self.all_directories = self.get_directories(self.directory, self.packages)
        else:
            # SampleView was not configured with a directory, but with a URL.
            # Therefore we don't have anything to serve here.
            self.all_directories = []

        await super().check_config()

    def file_response(
        self,
        full_path: PathLike,
        stat_result: os.stat_result,
        scope: Scope,
        status_code: int = 200,
    ) -> Response:
        response = super().file_response(
            full_path, stat_result, scope, status_code=status_code
        )
        # By default no caching header is set by starlette. Therefore browser
        # default behaviour kicks in, however Chrome seems to be rather
        # aggressive in that regard and does not even check for a changed ETag.
        # We use the cache control header here to avoid having an old version
        # in the browser.
        response.headers["Cache-Control"] = "no-cache"
        return response


def provide_sample_view(
    lifedata_api: Project = Depends(provide_project),
) -> Optional[SampleView]:
    return lifedata_api.get_sample_view()


def provide_base_url(
    request: Request,
) -> str:
    BASE_URL = os.environ.get("BASE_URL", None)
    if not BASE_URL:
        return str(request.base_url)
    return BASE_URL


class SampleViewConfig(BaseModel):
    # name is the name of a builtin sample view component
    # Exactly one of name or url must be set
    name: Optional[str]
    url: Optional[str]
    args: Any


@router.get("/sampleview/config/", response_model=SampleViewConfig)
def config(
    sample_view: Optional[SampleView] = Depends(provide_sample_view),
    base_url: str = Depends(provide_base_url),
) -> SampleViewConfig:
    if sample_view is None:
        sample_view = SampleView(
            name="error",
            args={
                "message": "Please configure `get_sample_view` in your `lifedata_api.py` file"
            },
        )

    name: Optional[str]
    url: Optional[str]

    if sample_view.name is not None:
        name = sample_view.name
        url = None
    else:
        name = None
        static_url = f"{base_url}api/sampleview/component/static/"
        url = sample_view.url if sample_view.url else static_url
    args = sample_view.args if sample_view.args is not None else {}
    return SampleViewConfig(
        name=name,
        url=url,
        args=args,
    )
