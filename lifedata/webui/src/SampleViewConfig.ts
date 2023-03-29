export type SampleViewConfig =
  | {
      name: string;
      url?: null;
      args: object;
    }
  | { name?: null; url: string; args: object };

export type QueuedSamples = {
  queued_samples: object;
};
