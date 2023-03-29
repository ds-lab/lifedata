import importlib.util
import os
from pathlib import Path
from typing import List
from typing import Optional

from loguru import logger

from .sample_view import SampleView
from lifedata.annotations.annotation import Annotation
from lifedata.annotations.authentication import TokenDecoder
from lifedata.annotations.queriedsample import QueriedSample
from lifedata.annotations.sample import Sample
from lifedata.annotations.skip import Skip
from lifedata.lifedata_api import AnnotationQueue
from lifedata.lifedata_api.label_config import LabelConfig
from lifedata.lifedata_api.ui_string_definition import UiStringDefinition


class Project:
    def __init__(self, lifedata_api_module):
        self._api = lifedata_api_module

    def get_label_metadata(self) -> LabelConfig:
        config = self._api.get_label_metadata()
        if isinstance(config, dict):
            config = LabelConfig(**config)
        return config

    def get_annotation_queues_config(self) -> List[AnnotationQueue]:
        if not hasattr(self._api, "get_annotation_queues_config"):
            return []
        return self._api.get_annotation_queues_config()

    def get_string_definitions(self) -> UiStringDefinition:
        return self._api.get_string_definitions()

    def get_all_sample_ids(self) -> List[str]:
        return self._api.get_all_sample_ids()

    def read_sample_for_display(self, sample_id: str) -> Optional[dict]:
        return self._api.read_sample_for_display(sample_id)

    def get_queryset(self) -> List[QueriedSample]:
        return self._api.get_queryset()

    def recreate_queryset(self) -> None:
        return self._api.recreate_queryset()

    def get_training_progress(self) -> Optional[bool]:
        return self._api.get_training_progress()

    def write_label_state(
        self,
        annotated: List[Annotation],
        unannotated: List[Sample],
        skipped: List[Skip],
    ) -> None:
        return self._api.write_label_state(annotated, unannotated, skipped)

    def get_labeled_state(self) -> List[Annotation]:
        return self._api.get_labeled_state()

    def get_sample_view(self) -> Optional[SampleView]:
        try:
            return self._api.get_sample_view()
        except Exception:
            logger.exception("Tried to load `get_sample_view` but got an exception.")
            return None

    def get_auth_token_decoder(self) -> Optional[TokenDecoder]:
        if hasattr(self._api, "get_auth_token_decoder"):
            return self._api.get_auth_token_decoder()
        return None


def get_environment_apipath():
    if "LIFEDATA_API_PATH" in os.environ:
        return Path(os.environ["LIFEDATA_API_PATH"])


def APINotFoundError() -> str:
    return (
        "File was not found in the current directory and the directories above. \n\t"
        + "Possibilities to fix this error:  \n\t"
        + "- Add LIFEDATA_API_PATH with absolute path to configuration file to environment variables (e.g. C:/Projects/mylifedataproject/lifedata_api.py) \n\t"
        + "- Change the working directory to the folder with the current project instance (e.g. C:/Projects/mylifedataproject)"
    )


def get_project_api_path(startpath):
    """
    Look for the ``lifedata_api.py`` file, starting in ``startpath``. If
    the file does not exist in the given directory, we look in every parent
    directory if it exists there.

    If a ``lifedata_api.py`` file is found, the path to it is returned.
    Otherwise an error is raised.
    """

    search_path = startpath
    while search_path:
        if search_path == search_path.parent:
            raise Exception(APINotFoundError())
        suggested_path = search_path / "lifedata_api.py"
        suggested_path_subfolder = search_path / "lifedata_api" / "lifedata_api.py"
        if suggested_path.exists():
            return suggested_path
        elif suggested_path_subfolder.exists():
            return suggested_path_subfolder
        else:
            search_path = search_path.parent


def load_project_api() -> Project:
    if get_environment_apipath():
        project_api_file_path = get_environment_apipath()
    else:
        project_api_file_path = get_project_api_path(Path.cwd())
        os.environ["LIFEDATA_API_PATH"] = str(project_api_file_path)

    spec = importlib.util.spec_from_file_location(
        "lifedata_api", str(project_api_file_path)
    )
    module = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(module)  # type: ignore

    return Project(module)
