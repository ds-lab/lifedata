import SelectLabelForm from "./SelectLabelForm";

import React from "react";
import { action } from "@storybook/addon-actions";
import exampleLabelConfig from "../stories/test_label_config.json";
import exampleAnnotationQueueConfig from "../stories/test_button_config.json";
import exampleEmptyAnnotationQueueConfig from "../stories/test_empty_button_config.json";
import exampleStringConfig from "../stories/test_string_config.json";
export default {
  title: "Select Label Form",
  component: SelectLabelForm,
};

export const Default = () => {
  return (
    <SelectLabelForm
      labelConfig={exampleLabelConfig}
      annotationQueueConfig={exampleAnnotationQueueConfig}
      onSubmit={action("submit")}
      onConsult={action("consult")}
      onSkip={action("skip")}
      uiStringsConfig={exampleStringConfig}
    />
  );
};

export const SingleButtonConfig = () => {
  return (
    <SelectLabelForm
      labelConfig={exampleLabelConfig}
      annotationQueueConfig={exampleEmptyAnnotationQueueConfig}
      onSubmit={action("submit")}
      onConsult={action("consult")}
      onSkip={action("skip")}
      uiStringsConfig={exampleStringConfig}
    />
  );
};

export const Submitting = () => {
  return (
    <SelectLabelForm
      labelConfig={exampleLabelConfig}
      annotationQueueConfig={exampleAnnotationQueueConfig}
      onSubmit={action("submit")}
      onConsult={action("consult")}
      onSkip={action("skip")}
      submitting
      uiStringsConfig={exampleStringConfig}
    />
  );
};
