import { Box } from "@material-ui/core";
import TextField from "@material-ui/core/TextField";
import Autocomplete, {
  createFilterOptions,
} from "@material-ui/lab/Autocomplete";
import React, { useState } from "react";
import { Label, LabelGroup } from "../labels";
import { StringConfig } from "../ui_strings";

type FlatLabel = {
  label: Label;
  subgroup: LabelGroup;
  group: LabelGroup;
};

export default function SearchLabel({
  labelGroups,
  onSelect,
  uiStringsConfig,
}: {
  labelGroups: LabelGroup[];
  onSelect: (label: Label) => void;
  uiStringsConfig: StringConfig;
}) {
  const flatLabels: FlatLabel[] = [];

  function addLabelGroup(group: LabelGroup, topLevelGroup: LabelGroup) {
    group.labels.forEach((label) => {
      flatLabels.push({
        label,
        subgroup: group,
        group: topLevelGroup,
      });
    });
    group.subgroups.forEach((g) => addLabelGroup(g, topLevelGroup));
  }

  labelGroups.forEach((g) => addLabelGroup(g, g));

  const [inputValue, setInputValue] = useState("");

  const filterOptions = createFilterOptions({
    stringify: (option: FlatLabel) => `${option.label.name} ${option.label.id}`,
  });

  return (
    <Autocomplete
      id="search-label"
      options={flatLabels}
      filterOptions={filterOptions}
      autoHighlight
      getOptionLabel={(option) => option.label.id}
      groupBy={(option) => option.group.name}
      renderOption={(option) => (
        <React.Fragment>
          {option.label.name}
          <Box paddingLeft={1} style={{ fontSize: "0.7em" }}>
            {option.label.id}
          </Box>
        </React.Fragment>
      )}
      renderInput={(params) => (
        <TextField
          {...params}
          label={uiStringsConfig.label_search_bar_text}
          variant="outlined"
          inputProps={{
            ...params.inputProps,
            // disable autocomplete and autofill
            autoComplete: "off",
          }}
        />
      )}
      value={null}
      inputValue={inputValue}
      onInputChange={(_, value) => {
        setInputValue(value);
      }}
      onChange={(_, value) => {
        setInputValue("");
        if (value === null) return;
        onSelect(value.label);
      }}
    />
  );
}
