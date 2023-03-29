from dataclasses import dataclass


@dataclass
class UiStringDefinition:
    """
    A label config is the definition of labels for display in the UI.
    """

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
