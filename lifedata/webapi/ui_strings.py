from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from .providers import provide_project
from lifedata.lifedata_api import UiStringDefinition
from lifedata.lifedata_api.api import Project

router = APIRouter()


class UIStringsConfig(BaseModel):
    project_title: str
    sample_title: str
    label_request_text: str
    label_request_text_2: str
    sample_loading_message: str
    sample_not_found_message: str
    sample_not_loaded_message: str
    all_samples_annotated: str
    skip_button_hover_text: str
    skip_button_text: str
    annotate_button_text: str
    label_search_bar_text: str
    selected_labels: str
    no_initial_samples: str
    annotation_stored_text: str
    annotation_storage_failed_text: str
    consulting_text: str
    consulting_failed_text: str
    sample_skipped_text: str
    sample_skipped_fail_text: str
    logout_text: str


def provide_ui_strings(
    lifedata_api: Project = Depends(provide_project),
) -> UiStringDefinition:
    return lifedata_api.get_string_definitions()


@router.get("/sampleview/strings/", response_model=UIStringsConfig)
def string_config(
    string_definition: UiStringDefinition = Depends(provide_ui_strings),
) -> UIStringsConfig:
    return UIStringsConfig(
        project_title=string_definition.project_title,
        sample_title=string_definition.sample_title,
        label_request_text=string_definition.label_request_text,
        label_request_text_2=string_definition.label_request_text_2,
        sample_loading_message=string_definition.sample_loading_message,
        sample_not_found_message=string_definition.sample_not_found_message,
        sample_not_loaded_message=string_definition.sample_not_loaded_message,
        all_samples_annotated=string_definition.all_samples_annotated,
        skip_button_hover_text=string_definition.skip_button_hover_text,
        skip_button_text=string_definition.skip_button_text,
        annotate_button_text=string_definition.annotate_button_text,
        label_search_bar_text=string_definition.label_search_bar_text,
        selected_labels=string_definition.selected_labels,
        no_initial_samples=string_definition.no_initial_samples,
        annotation_stored_text=string_definition.annotation_stored_text,
        annotation_storage_failed_text=string_definition.annotation_storage_failed_text,
        consulting_text=string_definition.consulting_text,
        consulting_failed_text=string_definition.consulting_failed_text,
        sample_skipped_text=string_definition.sample_skipped_text,
        sample_skipped_fail_text=string_definition.sample_skipped_fail_text,
        logout_text=string_definition.logout_text,
    )
