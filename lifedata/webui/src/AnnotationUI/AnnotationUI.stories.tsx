import { action } from "@storybook/addon-actions";
import React from "react";
import MockAppContext from "../MockAppContext";
import testSample1 from "../stories/test_sample_01.json";
import testUser01 from "../stories/test_user_01.json";
import exampleLabelConfig from "../stories/test_label_config.json";
import exampleAnnotationQueueConfig from "../stories/test_button_config.json";
import exampleEmptyButtonConfig from "../stories/test_empty_button_config.json";
import exampleStringConfig from "../stories/test_string_config.json";
import exampleAnnotationCountConfig from "../stories/test_annotation_count.json";
import { AnnotationCountTable } from "../AnnotationCountTable";
import exampleQueuedSamples from "../stories/test_queued_samples.json";

import {
  AnnotateSample,
  SampleLoading,
  FileNotFound,
  NoInitialSamples,
  UIChrome,
} from "./AnnotationUI";

export default {
  title: "Annotation UI",
};

const sampleViewConfig = {
  name: "image-by-url",
  args: {},
};

const customSampleViewConfig = {
  url: "http://localhost:3010",
  args: {},
};

const csvSampleSample = {
  id: "csv01",
  data: `\
A,B
1.0,1.5
2.0,3.5`,
};

export const Loading = () => (
  <MockAppContext>
    <UIChrome
      user={testUser01}
      uiStringsConfig={exampleStringConfig}
      annotationCount={
        <AnnotationCountTable annotationCount={exampleAnnotationCountConfig} />
      }
      onLogout={action("logout")}
    >
      <SampleLoading uiStringsConfig={exampleStringConfig} />
    </UIChrome>
  </MockAppContext>
);

export const SampleLoaded = () => (
  <MockAppContext>
    <UIChrome
      user={testUser01}
      uiStringsConfig={exampleStringConfig}
      annotationCount={
        <AnnotationCountTable annotationCount={exampleAnnotationCountConfig} />
      }
      onLogout={action("logout")}
    >
      <AnnotateSample
        sample={testSample1}
        onSubmit={action("submit")}
        onConsult={action("consult")}
        onSkip={action("skip")}
        sampleViewConfig={sampleViewConfig}
        labelConfig={exampleLabelConfig}
        annotationQueueConfig={exampleAnnotationQueueConfig}
        uiStringsConfig={exampleStringConfig}
        queuedSamples={exampleQueuedSamples}
      />
    </UIChrome>
  </MockAppContext>
);

export const CustomSampleViewLoaded = () => (
  <MockAppContext>
    <UIChrome
      user={testUser01}
      uiStringsConfig={exampleStringConfig}
      annotationCount={
        <AnnotationCountTable annotationCount={exampleAnnotationCountConfig} />
      }
      onLogout={action("logout")}
    >
      <AnnotateSample
        sample={csvSampleSample}
        onSubmit={action("submit")}
        onConsult={action("consult")}
        onSkip={action("skip")}
        sampleViewConfig={customSampleViewConfig}
        labelConfig={exampleLabelConfig}
        annotationQueueConfig={exampleAnnotationQueueConfig}
        uiStringsConfig={exampleStringConfig}
        queuedSamples={exampleQueuedSamples}
      />
    </UIChrome>
  </MockAppContext>
);

export const ErrorInSampleViewConfig = () => (
  <MockAppContext>
    <UIChrome
      user={testUser01}
      uiStringsConfig={exampleStringConfig}
      annotationCount={
        <AnnotationCountTable annotationCount={exampleAnnotationCountConfig} />
      }
      onLogout={action("logout")}
    >
      <AnnotateSample
        sample={testSample1}
        onSubmit={action("submit")}
        onConsult={action("consult")}
        onSkip={action("skip")}
        sampleViewConfig={{
          name: "error",
          args: {
            message:
              "Please configure `get_sample_view` in your `lifedata_api.py` file",
          },
        }}
        labelConfig={exampleLabelConfig}
        annotationQueueConfig={exampleAnnotationQueueConfig}
        uiStringsConfig={exampleStringConfig}
        queuedSamples={exampleQueuedSamples}
      />
    </UIChrome>
  </MockAppContext>
);

export const SingleButtonConfig = () => (
  <MockAppContext>
    <UIChrome
      user={testUser01}
      uiStringsConfig={exampleStringConfig}
      annotationCount={
        <AnnotationCountTable annotationCount={exampleAnnotationCountConfig} />
      }
      onLogout={action("logout")}
    >
      <AnnotateSample
        sample={testSample1}
        onSubmit={action("submit")}
        onConsult={action("consult")}
        onSkip={action("skip")}
        sampleViewConfig={sampleViewConfig}
        labelConfig={exampleLabelConfig}
        annotationQueueConfig={exampleEmptyButtonConfig}
        uiStringsConfig={exampleStringConfig}
        queuedSamples={exampleQueuedSamples}
      />
    </UIChrome>
  </MockAppContext>
);

export const AnnotationSubmitting = () => (
  <MockAppContext>
    <UIChrome
      user={testUser01}
      uiStringsConfig={exampleStringConfig}
      annotationCount={
        <AnnotationCountTable annotationCount={exampleAnnotationCountConfig} />
      }
      onLogout={action("logout")}
    >
      <AnnotateSample
        sample={testSample1}
        submitting
        onSubmit={action("submit")}
        onConsult={action("consult")}
        onSkip={action("skip")}
        sampleViewConfig={sampleViewConfig}
        labelConfig={exampleLabelConfig}
        annotationQueueConfig={exampleAnnotationQueueConfig}
        uiStringsConfig={exampleStringConfig}
        queuedSamples={exampleQueuedSamples}
      />
    </UIChrome>
  </MockAppContext>
);

export const NoInitialSamplesFound = () => (
  <MockAppContext>
    <UIChrome
      user={testUser01}
      uiStringsConfig={exampleStringConfig}
      annotationCount={
        <AnnotationCountTable annotationCount={exampleAnnotationCountConfig} />
      }
      onLogout={action("logout")}
    >
      <NoInitialSamples uiStringsConfig={exampleStringConfig} />
    </UIChrome>
  </MockAppContext>
);

export const FoundNoFile = () => (
  <MockAppContext>
    <UIChrome
      user={testUser01}
      uiStringsConfig={exampleStringConfig}
      annotationCount={
        <AnnotationCountTable annotationCount={exampleAnnotationCountConfig} />
      }
      onLogout={action("logout")}
    >
      <FileNotFound uiStringsConfig={exampleStringConfig} />
    </UIChrome>
  </MockAppContext>
);
