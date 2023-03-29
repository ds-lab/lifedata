export type AnnotationQueueConfig = {
  annotation_queue_config: AnnotationQueueDefinition[];
};

export type AnnotationQueueDefinition = {
  queue_name: string;
  short_description: string;
};

export type QueuedSamples = {
  queued_samples: QueuedSample[];
};

export type QueuedSample = {
  sample_id: string;
  queue_name: string;
  requested_by: string;
};
