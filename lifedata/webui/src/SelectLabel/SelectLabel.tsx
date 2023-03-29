import { Box, Typography } from "@material-ui/core";
import React from "react";
import { Label, LabelGroup } from "../labels";
import LabelChip from "./LabelChip";

function DisplayLabelGroup({
  group,
  level,
  selected,
  onSelect,
  onDeselect,
  disabled = false,
}: {
  group: LabelGroup;
  level: number;
  selected: Label[];
  onSelect: (label: Label) => void;
  onDeselect: (label: Label) => void;
  disabled?: boolean;
}) {
  return (
    <React.Fragment>
      <Box marginBottom={1}>
        {level === 0 && (
          <Box paddingBottom={1} clone>
            <Typography variant="h6">{group.name}</Typography>
          </Box>
        )}
        <Box display="flex" alignItems="left" flexWrap="wrap">
          {group.labels.length > 0 &&
            group.labels.map((label) => (
              <LabelChip
                key={label.id}
                label={label}
                onSelect={onSelect}
                onDeselect={onDeselect}
                selected={selected.some(({ id }) => id === label.id)}
                disabled={disabled}
              />
            ))}
        </Box>
      </Box>
      {group.subgroups.map((g) => (
        <DisplayLabelGroup
          key={g.id}
          group={g}
          level={level + 1}
          onSelect={onSelect}
          onDeselect={onDeselect}
          selected={selected}
          disabled={disabled}
        />
      ))}
    </React.Fragment>
  );
}

export default function SelectLabel({
  labelGroups,
  ...props
}: {
  labelGroups: LabelGroup[];
  selected: Label[];
  onSelect: (label: Label) => void;
  onDeselect: (label: Label) => void;
  disabled?: boolean;
}) {
  return (
    <Box>
      {labelGroups.map((g) => (
        <DisplayLabelGroup key={g.id} group={g} level={0} {...props} />
      ))}
    </Box>
  );
}
