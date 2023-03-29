import { Box, Button, CircularProgress } from "@material-ui/core";
import ButtonGroup from "@material-ui/core/ButtonGroup";
import ArrowDropDownIcon from "@material-ui/icons/ArrowDropDown";
import ClickAwayListener from "@material-ui/core/ClickAwayListener";
import MenuList from "@material-ui/core/MenuList";
import MenuItem from "@material-ui/core/MenuItem";
import Popper from "@material-ui/core/Popper";
import React, { useCallback } from "react";
import { StringConfig } from "../ui_strings";
import { AnnotationQueueConfig } from "../queues";
import { Label } from "../labels";

export default function SubmitButton({
  annotationQueueConfig,
  onSubmit,
  onConsult,
  selected,
  submitting = false,
  uiStringsConfig,
}: {
  annotationQueueConfig: AnnotationQueueConfig;
  onSubmit: (labels: Label[]) => void;
  onConsult: (queue_name: string, labels: Label[]) => void;
  selected: any;
  submitting?: boolean;
  uiStringsConfig: StringConfig;
}) {
  let annotationQueueDefinition =
    annotationQueueConfig["annotation_queue_config"];
  const annotateDefinition = {
    queue_name: "annotate",
    short_description: uiStringsConfig.annotate_button_text,
  };

  annotationQueueDefinition = [
    annotateDefinition,
    ...annotationQueueDefinition,
  ];

  const canSubmit = !submitting && selected.length > 0;
  const doSubmit = useCallback(() => {
    onSubmit(selected);
  }, [selected, onSubmit]);

  const [selectedIndex, setSelectedIndex] = React.useState(0);
  const [open, setOpen] = React.useState(false);
  const anchorRef = React.useRef<HTMLDivElement>(null);

  const doConsult = useCallback(() => {
    onConsult(annotationQueueDefinition[selectedIndex].queue_name, selected);
  }, [annotationQueueDefinition, selected, onConsult, selectedIndex]);

  if (annotationQueueDefinition.length === 1) {
    return (
      <Box>
        <Button
          variant="contained"
          color="primary"
          onClick={doSubmit}
          disabled={!canSubmit}
        >
          {annotateDefinition.short_description}
          {submitting && (
            <Box marginX={1} clone>
              <CircularProgress size="1em" />
            </Box>
          )}
        </Button>
      </Box>
    );
  } else {
    const handleClick = () => {
      if (selectedIndex === 0) {
        doSubmit();
      } else {
        doConsult();
      }
    };

    const handleToggle = () => {
      setOpen((prevOpen) => !prevOpen);
    };

    const handleClose = (event: React.MouseEvent<Document, MouseEvent>) => {
      if (
        anchorRef.current &&
        anchorRef.current.contains(event.target as HTMLElement)
      ) {
        return;
      }

      setOpen(false);
    };

    const handleMenuItemClick = (
      event: React.MouseEvent<HTMLLIElement, MouseEvent>,
      index: number
    ) => {
      setSelectedIndex(index);
      setOpen(false);
    };
    return (
      <Box>
        <ButtonGroup
          variant="contained"
          color="primary"
          ref={anchorRef}
          aria-label="split button"
        >
          <Button onClick={handleClick} disabled={!canSubmit}>
            {annotationQueueDefinition[selectedIndex].short_description}
          </Button>
          <Button
            disabled={submitting ? true : false}
            color={!canSubmit ? "default" : "primary"}
            size="small"
            aria-controls={open ? "split-button-menu" : undefined}
            aria-expanded={open ? "true" : undefined}
            aria-label="select merge strategy"
            aria-haspopup="menu"
            onClick={handleToggle}
          >
            <ArrowDropDownIcon />
          </Button>
        </ButtonGroup>
        {submitting && (
          <Box marginX={1} clone>
            <CircularProgress size="1em" />
          </Box>
        )}
        <Popper
          open={open}
          anchorEl={anchorRef.current}
          role={undefined}
          transition
          disablePortal
          style={{ zIndex: 999, backgroundColor: "white" }}
        >
          {({ TransitionProps, placement }) => (
            <ClickAwayListener onClickAway={handleClose}>
              <MenuList id="split-button-menu">
                {annotationQueueDefinition.map((itemConfig, index) => (
                  <MenuItem
                    key={itemConfig.short_description}
                    onClick={(event) => handleMenuItemClick(event, index)}
                  >
                    {itemConfig.short_description}
                  </MenuItem>
                ))}
              </MenuList>
            </ClickAwayListener>
          )}
        </Popper>
      </Box>
    );
  }
}
