import { action } from "@storybook/addon-actions";
import React from "react";
import { makeLabelGroups } from "../labels";
import SearchLabel from "./SearchLabel";
import exampleLabelConfig from "../stories/test_label_config.json";
import { StringConfig } from "../ui_strings";
import exampleStringConfig from "../stories/test_string_config.json";

export default {
  title: "Search Labels",
  component: SearchLabel,
};

const labelGroups = makeLabelGroups(exampleLabelConfig);

export const NoneSelected = () => {
  return (
    <SearchLabel
      labelGroups={labelGroups}
      onSelect={action("select")}
      uiStringsConfig={exampleStringConfig}
    />
  );
};
