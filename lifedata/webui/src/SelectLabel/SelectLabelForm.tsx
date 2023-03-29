import { Box, Button, CircularProgress, Typography } from "@material-ui/core";
import React, { useCallback, useState } from "react";
import { Label, makeLabelGroups, LabelConfig } from "../labels";
import { makeStyles } from "@material-ui/core/styles";
import LabelChip from "./LabelChip";
import SearchLabel from "./SearchLabel";
import SelectLabel from "./SelectLabel";
import Tooltip from "@material-ui/core/Tooltip";
import { AnnotationQueueConfig } from "../queues";
import SubmitButton from "./SubmitButton";
import { StringConfig } from "../ui_strings";

const useStyles = makeStyles((theme) => ({
  skipButton: {
    marginLeft: theme.spacing(1),
  },
}));

export default function SelectLabelForm({
  labelConfig,
  annotationQueueConfig,
  onSubmit,
  onConsult,
  onSkip,
  submitting = false,
  uiStringsConfig,
}: {
  labelConfig: LabelConfig;
  annotationQueueConfig: AnnotationQueueConfig;
  onSubmit: (labels: Label[]) => void;
  onConsult: (queue_name: string, labels: Label[]) => void;
  onSkip: () => void;
  submitting?: boolean;
  uiStringsConfig: StringConfig;
}) {
  const classes = useStyles();
  const labelGroups = makeLabelGroups(labelConfig);
  const [selected, setSelected] = useState<Label[]>([]);

  const handleSelect = useCallback(
    (label: Label) => {
      const newSelected = [...selected.filter((l) => l.id !== label.id), label];
      setSelected(newSelected);
    },
    [selected]
  );
  const handleDeselect = useCallback(
    (label: Label) => {
      const newSelected = selected.filter((l) => l.id !== label.id);
      setSelected(newSelected);
    },
    [selected]
  );

  const doSkip = useCallback(() => {
    onSkip();
  }, [onSkip]);

  const canSkip = !submitting;

  return (
    <Box>
      <Box>
        <Box marginY={1}>
          <Typography>{uiStringsConfig.label_request_text_2}</Typography>
        </Box>
        <Box display="flex" marginBottom={1} paddingY={1}>
          {selected.length > 0 ? (
            <React.Fragment>
              <Typography>{uiStringsConfig.selected_labels}</Typography>
              {selected.map((label) => (
                <Box display="inline" marginLeft={1} key={label.id}>
                  <LabelChip
                    label={label}
                    selected
                    onSelect={handleSelect}
                    onDeselect={handleDeselect}
                  />
                </Box>
              ))}
            </React.Fragment>
          ) : null}
        </Box>
        <Box
          display="flex"
          flexDirection="row"
          alignItems="flex-start"
          marginLeft={1}
        >
          <SubmitButton
            annotationQueueConfig={annotationQueueConfig}
            onSubmit={onSubmit}
            onConsult={onConsult}
            submitting={submitting}
            selected={selected}
            uiStringsConfig={uiStringsConfig}
          />
          <Tooltip
            title={
              <p style={{ fontSize: 13 }}>
                {uiStringsConfig.skip_button_hover_text}
              </p>
            }
          >
            <Button
              className={classes.skipButton}
              onClick={doSkip}
              disabled={!canSkip}
            >
              {uiStringsConfig.skip_button_text}
              {submitting && (
                <Box marginX={1} clone>
                  <CircularProgress size="1em" />
                </Box>
              )}
            </Button>
          </Tooltip>
        </Box>
      </Box>
      <Box marginTop={3}>
        <SearchLabel
          labelGroups={labelGroups}
          onSelect={handleSelect}
          uiStringsConfig={uiStringsConfig}
        />
      </Box>
      <Box marginTop={1}>
        <SelectLabel
          labelGroups={labelGroups}
          selected={selected}
          onSelect={handleSelect}
          onDeselect={handleDeselect}
          disabled={submitting}
        />
      </Box>
    </Box>
  );
}
