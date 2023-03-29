class AnnotationQueue:
    """
    Custom definition of annotation button in the annotation UI.
    Use this object to configure how the sample view will be provided to the frontend.
    """

    def __init__(self, queue_name: str, short_description: str):
        self.queue_name = queue_name
        self.short_description = short_description


class QueuedSample:
    """
    Sample for which the label(s) from a second user is requested.
    """

    def __init__(self, sample_id: str, queue_name: str, requested_by: str):
        self.sample_id = sample_id
        self.queue_name = queue_name
        self.requested_by = requested_by
