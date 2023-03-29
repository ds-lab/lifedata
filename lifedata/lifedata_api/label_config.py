from typing import List


class LabelConfig:
    """
    Definition of labels for display in the UI.
    """

    def __init__(self, labels: List[dict], label_type: str, data_type: str):
        self.labels = labels
        self.label_type = label_type
        self.data_type = data_type
