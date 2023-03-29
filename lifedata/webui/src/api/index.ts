import { SampleViewConfig } from "../SampleViewConfig";
import { LabelConfig } from "../labels";
import { StringConfig } from "../ui_strings";
import { AnnotationQueueConfig, QueuedSamples } from "../queues";
import { Label } from "../labels";
import { Sample } from "../Sample";
import { User } from "../User";
import { AnnotationCountDefinition } from "../counts";

export interface IApi {
  authenticate(token: string): Promise<User>;
  logout(): Promise<undefined>;

  getSampleByID(
    sampleId: string
  ): Promise<
    | { status: "no-initial-samples"; sample: null }
    | { status: "no-samples-left"; sample: null }
    | { status: "waiting-for-training-to-finish"; sample: null }
    | { status: "sample-not-found"; sample: null }
    | { status: "ok"; sample: Sample }
  >;
  getCurrentSample(): Promise<
    | { status: "no-initial-samples"; sample: null }
    | { status: "no-samples-left"; sample: null }
    | { status: "waiting-for-training-to-finish"; sample: null }
    | { status: "sample-not-found"; sample: null }
    | { status: "ok"; sample: Sample }
  >;
  submitSample(sample: Sample, labels: Label[]): Promise<undefined>;
  consultColleague(
    sample: Sample,
    queue_name: string,
    labels: Label[]
  ): Promise<undefined>;
  skipSample(sample: Sample): Promise<undefined>;
  getSampleViewConfig(): Promise<SampleViewConfig>;
  getLabels(): Promise<LabelConfig>;
  getAnnotationQueueConfig(): Promise<AnnotationQueueConfig>;
  getUiStrings(): Promise<StringConfig>;
  getAnnotationCount(): Promise<AnnotationCountDefinition>;
  getQueuedSamples(): Promise<QueuedSamples>;
}
