import { CircularProgress, Container, Typography } from "@material-ui/core";
import Box from "@material-ui/core/Box";
import Paper from "@material-ui/core/Paper";
import Alert from "@material-ui/lab/Alert";
import React from "react";
import { AnnotationQueueConfig, QueuedSamples } from "../queues";
import HeaderAppBar from "../HeaderAppBar";
import { Label, LabelConfig } from "../labels";
import { Sample } from "../Sample";
import SampleView from "../SampleView/SampleView";
import { SampleViewConfig } from "../SampleViewConfig";
import SelectLabelForm from "../SelectLabel/SelectLabelForm";
import { User } from "../User";
import { StringConfig } from "../ui_strings";

import { BrowserRouter as Router, Link } from "react-router-dom";

export function UIChrome({
  user,
  uiStringsConfig,
  onLogout,
  annotationCount,
  children,
}: {
  user: User;
  uiStringsConfig: StringConfig;
  annotationCount: React.ReactFragment;
  onLogout: () => void;
  children: React.ReactNode;
}) {
  return (
    <React.Fragment>
      <HeaderAppBar
        user={user}
        uiStringsConfig={uiStringsConfig}
        annotationCount={annotationCount}
        onLogout={onLogout}
      />
      <Box padding={3} clone>
        <Paper elevation={1}>{children}</Paper>
      </Box>
    </React.Fragment>
  );
}

export function SampleLoading({
  uiStringsConfig,
}: {
  uiStringsConfig: StringConfig;
}) {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      paddingY={10}
    >
      <CircularProgress size={64} />
      <Box marginTop={2}>
        <Typography>{uiStringsConfig.sample_loading_message}</Typography>
      </Box>
    </Box>
  );
}

export function FileNotFound({
  uiStringsConfig,
}: {
  uiStringsConfig: StringConfig;
}) {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      paddingY={10}
    >
      <Box marginTop={2}>
        <Alert severity="error">
          {uiStringsConfig.sample_not_found_message}
        </Alert>
      </Box>
    </Box>
  );
}

export function SampleLoadingError({
  uiStringsConfig,
}: {
  uiStringsConfig: StringConfig;
}) {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      paddingY={10}
    >
      <Box marginTop={2}>
        <Alert severity="error">
          {uiStringsConfig.sample_not_loaded_message}
        </Alert>
      </Box>
    </Box>
  );
}

export function NoInitialSamples({
  uiStringsConfig,
}: {
  uiStringsConfig: StringConfig;
}) {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      paddingY={10}
    >
      <Box marginTop={2}>
        <Alert severity="error"> {uiStringsConfig.no_initial_samples}</Alert>
      </Box>
    </Box>
  );
}

export function NoStringConfig() {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      paddingY={10}
    >
      <Box marginTop={2}>
        <Alert severity="error">
          {" "}
          No sting configuration was found please add a string definition for
          the user interface in your project instance.
        </Alert>
      </Box>
    </Box>
  );
}

export function NoSamplesLeft({
  uiStringsConfig,
}: {
  uiStringsConfig: StringConfig;
}) {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      paddingY={10}
    >
      <Box marginTop={2}>
        <Alert>{uiStringsConfig.all_samples_annotated}</Alert>
      </Box>
    </Box>
  );
}

export function AnnotateSample({
  sample,
  onSubmit,
  onConsult,
  onSkip,
  submitting = false,
  labelConfig,
  annotationQueueConfig,
  sampleViewConfig,
  uiStringsConfig,
  queuedSamples,
}: {
  sample: Sample;
  onSubmit: (labels: Label[]) => void;
  onConsult: (queue_name: string, labels: Label[]) => void;
  onSkip: () => void;
  submitting?: boolean;
  labelConfig: LabelConfig;
  annotationQueueConfig: AnnotationQueueConfig;
  sampleViewConfig: SampleViewConfig;
  uiStringsConfig: StringConfig;
  queuedSamples: QueuedSamples;
}) {
  // NOTE: This is not the best way to do this therefore it needs a better implementation in state management
  // Reduce queuedSamplesList from object to list of unique sample_ids
  const uniqueQueuedList = Array.from(
    new Set(queuedSamples["queued_samples"].map((item) => item.sample_id))
  );

  // Create list of links to samples
  const queuedSamplesLinks = uniqueQueuedList.map((sample_id) => (
    <Router forceRefresh={true}>
      <Link
        style={{ display: "block", margin: "1rem 0" }}
        to={`/sample/${sample_id}`}
        key={sample_id}
      >
        {sample_id}
      </Link>
    </Router>
  ));

  // TODO remove this if consulting component is implemented
  console.log(queuedSamplesLinks);

  return (
    <React.Fragment>
      <Container>
        <Typography variant="h4" component="h2">
          {uiStringsConfig.sample_title} {sample.id}
        </Typography>
      </Container>
      {/* This is certainly not the prettiest display and therefore also needs to be changed.  */}
      {/* {queuedSamplesLinks} */}
      <Box paddingY={2}>
        <SampleView sample={sample} config={sampleViewConfig} />
      </Box>
      <Container>
        <Box marginTop={1}>
          <Typography variant="h5" component="p">
            {uiStringsConfig.label_request_text}
          </Typography>
          <SelectLabelForm
            labelConfig={labelConfig}
            annotationQueueConfig={annotationQueueConfig}
            onSubmit={onSubmit}
            onConsult={onConsult}
            onSkip={onSkip}
            submitting={submitting}
            uiStringsConfig={uiStringsConfig}
          />
        </Box>
      </Container>
    </React.Fragment>
  );
}
