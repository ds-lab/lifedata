import {
  Box,
  Chip,
  makeStyles,
  PopoverProps,
  Typography,
} from "@material-ui/core";
import { lightGreen } from "@material-ui/core/colors";
import DoneIcon from "@material-ui/icons/Done";
import InfoIcon from "@material-ui/icons/Info";
import {
  bindHover,
  bindPopover,
  usePopupState,
} from "material-ui-popup-state/hooks";
import Popover from "material-ui-popup-state/HoverPopover";
import React from "react";
import { Label, LabelGroup } from "../labels";

function getGroupChain(item: LabelGroup): LabelGroup[] {
  return [...(item.parent !== null ? getGroupChain(item.parent) : []), item];
}

export const useStyles = makeStyles((theme) => ({
  labelSelected: {
    "&:focus, &:hover": {
      backgroundColor: lightGreen[700],
    },
    "& .MuiChip-deleteIcon": {
      color: "white",
    },
    backgroundColor: lightGreen[600],
    color: "white",
  },
  infoIcon: {
    color: theme.palette.grey[500],
  },
}));

function LabelCriteriaPopover({
  label,
  ...props
}: { label: Label } & PopoverProps) {
  return (
    <Popover
      anchorOrigin={{
        vertical: "center",
        horizontal: "right",
      }}
      transformOrigin={{
        vertical: "center",
        horizontal: "left",
      }}
      // disableRestoreFocus
      {...props}
    >
      <Box margin={1} padding={1} maxWidth={500}>
        <Typography component="div">
          <Box marginBottom={1} fontWeight="bold">
            Categorization:
          </Box>
          <Box>
            {getGroupChain(label.parent).map((g, i) => (
              <Box key={i} paddingLeft={i * 2} component="div">
                {i !== 0 ? "⤷ " : ""}
                {g.name}
              </Box>
            ))}
          </Box>
          {label.criterias && (
            <Box marginTop={2}>
              <Typography component="div">
                <Box marginBottom={1} fontWeight="bold">
                  Criteria:
                </Box>
                {label.criterias.split("\n").map((line, i) => (
                  <Box key={i} marginBottom={1}>
                    {line}
                  </Box>
                ))}
              </Typography>
            </Box>
          )}
        </Typography>
      </Box>
    </Popover>
  );
}

export function LabelInfo({ label }: { label: Label }) {
  const popupState = usePopupState({
    variant: "popover",
    popupId: `labelHelpText_${label.id}`,
  });
  const classes = useStyles();

  return (
    <div>
      <InfoIcon {...bindHover(popupState)} className={classes.infoIcon} />
      <LabelCriteriaPopover label={label} {...bindPopover(popupState)} />
    </div>
  );
}

export default function LabelChip({
  label,
  selected = false,
  onSelect = (label) => null,
  onDeselect = (label) => null,
  disabled = false,
}: {
  label: Label;
  selected?: boolean;
  onSelect?: (label: Label) => void;
  onDeselect?: (label: Label) => void;
  disabled?: boolean;
}) {
  const classes = useStyles();

  return (
    <Box display="flex" alignItems="center" paddingBottom={1} paddingRight={2}>
      {selected ? (
        <Chip
          label={label.name}
          className={classes.labelSelected}
          onClick={() => {
            onDeselect(label);
          }}
          onDelete={() => {
            onDeselect(label);
          }}
          deleteIcon={<DoneIcon />}
          disabled={disabled}
        />
      ) : (
        <Chip
          label={label.name}
          variant="outlined"
          onClick={() => {
            onSelect(label);
          }}
          disabled={disabled}
        />
      )}
      <Box marginLeft={0.5}>
        <LabelInfo label={label} />
      </Box>
    </Box>
  );
}
