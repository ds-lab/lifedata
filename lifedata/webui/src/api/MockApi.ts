import { SampleViewConfig } from "../SampleViewConfig";
import { LabelConfig } from "../labels";
import { StringConfig } from "../ui_strings";
import { AnnotationQueueConfig, QueuedSamples } from "../queues";
import { Sample } from "../Sample";
import testSample01 from "../stories/test_sample_01.json";
import testUser01 from "../stories/test_user_01.json";
import exampleLabelConfig from "../stories/test_label_config.json";
import exampleAnnotationQueueConfig from "../stories/test_button_config.json";
import exampleStringConfig from "../stories/test_string_config.json";
import exampleAnnotationCountConfig from "../stories/test_annotation_count.json";
import { AnnotationCountDefinition } from "../counts";
import exampleQueuedSamples from "../stories/test_queued_samples.json";

import { User } from "../User";
import { IApi } from "./index";

export type MockAPIOptions = {
  delay?: number;
  failOnAuthenticate?: boolean;
  failOnSubmitSample?: boolean;
  failOnLoadSample?: boolean;
  samplesLeft?: boolean;
  noInitialSamplesFound?: boolean;
  fileNotFound?: boolean;
  sampleViewConfig?: SampleViewConfig;
  sampleLabels?: LabelConfig;
  annotationQueueConfig?: AnnotationQueueConfig;
  uiStringsConfig?: StringConfig;
  annotationCount?: AnnotationCountDefinition;
  queuedSamples?: QueuedSamples;
};

export default class MockAPI implements IApi {
  token: string | null = null;
  options: MockAPIOptions = {
    delay: 400,
    failOnAuthenticate: false,
    failOnSubmitSample: false,
    failOnLoadSample: false,
    samplesLeft: true,
    noInitialSamplesFound: false,
    fileNotFound: false,
    sampleViewConfig: {
      name: "image-by-url",
      args: {},
    },
    sampleLabels: exampleLabelConfig,
    annotationQueueConfig: exampleAnnotationQueueConfig,
    uiStringsConfig: exampleStringConfig,
    annotationCount: exampleAnnotationCountConfig,
    queuedSamples: exampleQueuedSamples,
  };

  constructor(options: Partial<MockAPIOptions> = {}) {
    this.options = Object.assign({}, this.options, options);
  }

  async authenticate(token: string) {
    return new Promise<User>((resolve, reject) => {
      setTimeout(() => {
        if (this.options.failOnAuthenticate) {
          reject();
        } else {
          resolve(testUser01 as User);
          this.token = token;
        }
      }, this.options.delay);
    });
  }

  async logout() {
    return Promise.resolve(undefined);
  }

  async getSampleByID(sampleId: string) {
    return new Promise<
      | { status: "no-initial-samples"; sample: null }
      | { status: "no-samples-left"; sample: null }
      | { status: "waiting-for-training-to-finish"; sample: null }
      | { status: "sample-not-found"; sample: null }
      | { status: "ok"; sample: Sample }
    >((resolve, reject) => {
      setTimeout(() => {
        if (this.options.failOnLoadSample) {
          reject();
        } else if (!this.options.samplesLeft) {
          resolve({ status: "no-samples-left", sample: null });
        } else if (this.options.noInitialSamplesFound) {
          resolve({ status: "no-initial-samples", sample: null });
        } else if (this.options.fileNotFound) {
          resolve({ status: "sample-not-found", sample: null });
        } else {
          resolve({ status: "ok", sample: { ...testSample01 } as Sample });
        }
      }, this.options.delay);
    });
  }

  async getCurrentSample() {
    return new Promise<
      | { status: "no-initial-samples"; sample: null }
      | { status: "no-samples-left"; sample: null }
      | { status: "waiting-for-training-to-finish"; sample: null }
      | { status: "sample-not-found"; sample: null }
      | { status: "ok"; sample: Sample }
    >((resolve, reject) => {
      setTimeout(() => {
        if (this.options.failOnLoadSample) {
          reject();
        } else if (!this.options.samplesLeft) {
          resolve({ status: "no-samples-left", sample: null });
        } else if (this.options.noInitialSamplesFound) {
          resolve({ status: "no-initial-samples", sample: null });
        } else if (this.options.fileNotFound) {
          resolve({ status: "sample-not-found", sample: null });
        } else {
          resolve({ status: "ok", sample: { ...testSample01 } as Sample });
        }
      }, this.options.delay);
    });
  }

  async submitSample() {
    return new Promise<undefined>((resolve, reject) => {
      setTimeout(() => {
        if (this.options.failOnSubmitSample) {
          reject();
        } else {
          resolve(undefined);
        }
      }, this.options.delay);
    });
  }

  async consultColleague() {
    return new Promise<undefined>((resolve, reject) => {
      setTimeout(() => {
        if (this.options.failOnSubmitSample) {
          reject();
        } else {
          resolve(undefined);
        }
      }, this.options.delay);
    });
  }

  async skipSample() {
    return new Promise<undefined>((resolve, reject) => {
      setTimeout(() => {
        if (this.options.failOnSubmitSample) {
          reject();
        } else {
          resolve(undefined);
        }
      }, this.options.delay);
    });
  }

  async getSampleViewConfig() {
    return new Promise<SampleViewConfig>((resolve, reject) => {
      setTimeout(() => {
        if (this.options.sampleViewConfig) {
          resolve(this.options.sampleViewConfig);
        } else {
          reject();
        }
      }, this.options.delay);
    });
  }

  async getLabels() {
    return new Promise<LabelConfig>((resolve, reject) => {
      setTimeout(() => {
        if (this.options.sampleLabels) {
          resolve(this.options.sampleLabels);
        } else {
          reject();
        }
      }, this.options.delay);
    });
  }

  async getAnnotationQueueConfig() {
    return new Promise<AnnotationQueueConfig>((resolve, reject) => {
      setTimeout(() => {
        if (this.options.annotationQueueConfig) {
          resolve(this.options.annotationQueueConfig);
        } else {
          reject();
        }
      }, this.options.delay);
    });
  }
  async getUiStrings() {
    return new Promise<any>((resolve, reject) => {
      setTimeout(() => {
        if (this.options.uiStringsConfig) {
          resolve(this.options.uiStringsConfig);
        } else {
          reject();
        }
      }, this.options.delay);
    });
  }

  async getQueuedSamples() {
    return new Promise<QueuedSamples>((resolve, reject) => {
      setTimeout(() => {
        if (this.options.queuedSamples) {
          resolve(this.options.queuedSamples);
        } else {
          reject();
        }
      }, this.options.delay);
    });
  }

  async getAnnotationCount() {
    return new Promise<AnnotationCountDefinition>((resolve, reject) => {
      setTimeout(() => {
        if (this.options.annotationCount) {
          resolve(this.options.annotationCount);
        } else {
          reject();
        }
      }, this.options.delay);
    });
  }
}
