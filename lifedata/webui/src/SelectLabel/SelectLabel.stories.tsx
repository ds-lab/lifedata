import SelectLabel from "./SelectLabel";
import React from "react";
import { action } from "@storybook/addon-actions";
import exampleLabelConfig from "../stories/test_label_config.json";
import { makeLabelGroups } from "../labels";

export default {
  title: "Select Labels",
  component: SelectLabel,
};

const labelGroups = makeLabelGroups(exampleLabelConfig);

export const NoneSelected = () => {
  return (
    <SelectLabel
      labelGroups={labelGroups}
      selected={[]}
      onSelect={action("select")}
      onDeselect={action("deselect")}
    />
  );
};

export const SomeSelected = () => {
  return (
    <SelectLabel
      labelGroups={labelGroups}
      selected={[labelGroups[0].labels[0]]}
      onSelect={action("select")}
      onDeselect={action("deselect")}
    />
  );
};

export const SomeSelectedAndDisabled = () => {
  return (
    <SelectLabel
      labelGroups={labelGroups}
      selected={[labelGroups[0].labels[0]]}
      onSelect={action("select")}
      onDeselect={action("deselect")}
      disabled
    />
  );
};
