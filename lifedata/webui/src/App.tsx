import { CssBaseline } from "@material-ui/core";
import { SnackbarProvider, useSnackbar } from "notistack";
import React, { useEffect } from "react";
import { AppStateProvider } from "./AppState/AppState";
import { AppDependencies } from "./AppState/Dependencies";
import {
  useSamplesLeft,
  useInitialSamplesFound,
  useCurrentSample,
  useIsSampleLoading,
  useIsSubmitting,
  useSubmitSample,
  useConsultColleague,
  useSkipSample,
  useHasSampleError,
  useFileNotFound,
  useLoadNewSample,
  useIsSamplePending,
  useAnnotationCount,
  useQueuedSamples,
} from "./AppState/SampleState";
import { useLogoutAction, useUser } from "./AppState/UserState";
import {
  useLabelConfig,
  useSampleViewConfig,
  useAnnotationQueueConfig,
  useUiStringsConfig,
} from "./AppState/ProjectState";
import {
  NoInitialSamples,
  NoSamplesLeft,
  AnnotateSample,
  SampleLoading,
  UIChrome,
  SampleLoadingError,
  FileNotFound,
  NoStringConfig,
} from "./AnnotationUI/AnnotationUI";
import { Label } from "./labels";
import LoginScreen from "./LoginScreen/LoginScreen";
import BackendApi from "./api/BackendApi";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
  useParams,
} from "react-router-dom";
import { AnnotationCountTable } from "./AnnotationCountTable";
import { StringConfig } from "./ui_strings";

/**
 * Provide a wrapper with common configuration (like theming and other context
 * where necessary)
 */
export function AppContext({
  children,
  dependencies,
}: {
  children: React.ReactNode;
  dependencies?: AppDependencies;
}) {
  return (
    <SnackbarProvider
      autoHideDuration={5000}
      maxSnack={5}
      anchorOrigin={{ horizontal: "center", vertical: "top" }}
    >
      <AppStateProvider dependencies={dependencies}>
        <CssBaseline />
        {children}
      </AppStateProvider>
    </SnackbarProvider>
  );
}

export function AnnotationContent({
  uiStringsConfig,
}: {
  uiStringsConfig: StringConfig;
}) {
  const sample = useCurrentSample();
  const isLoading = useIsSampleLoading();
  const submitting = useIsSubmitting();
  const sampleError = useHasSampleError();
  const fileNotFound = useFileNotFound();
  const sampleViewConfig = useSampleViewConfig();
  const labelConfig = useLabelConfig();
  const annotationQueueConfig = useAnnotationQueueConfig();
  const queuedSamples = useQueuedSamples();

  const submitSample = useSubmitSample();
  const consultColleague = useConsultColleague();
  const skipSample = useSkipSample();

  const { enqueueSnackbar } = useSnackbar();

  const handleSubmit = async (labels: Label[]) => {
    try {
      await submitSample(labels);
      enqueueSnackbar(uiStringsConfig.annotation_stored_text, {
        variant: "success",
      });
    } catch (e) {
      enqueueSnackbar(uiStringsConfig.annotation_storage_failed_text, {
        variant: "error",
      });
    }
  };

  const handleConsult = async (queue_name: string, labels: Label[]) => {
    try {
      await consultColleague(queue_name, labels);
      enqueueSnackbar(uiStringsConfig.consulting_text, {
        variant: "success",
      });
    } catch (e) {
      enqueueSnackbar(uiStringsConfig.consulting_failed_text, {
        variant: "error",
      });
    }
  };

  const handleSkip = async () => {
    try {
      await skipSample();
      enqueueSnackbar(uiStringsConfig.sample_skipped_text, {
        variant: "success",
      });
    } catch (e) {
      enqueueSnackbar(uiStringsConfig.sample_skipped_fail_text, {
        variant: "error",
      });
    }
  };

  return !isLoading &&
    labelConfig !== null &&
    annotationQueueConfig !== null &&
    sampleViewConfig !== null &&
    queuedSamples !== null &&
    sample ? (
    <AnnotateSample
      sample={sample}
      onSubmit={handleSubmit}
      onConsult={handleConsult}
      onSkip={handleSkip}
      submitting={submitting}
      sampleViewConfig={sampleViewConfig}
      annotationQueueConfig={annotationQueueConfig}
      queuedSamples={queuedSamples}
      labelConfig={labelConfig}
      uiStringsConfig={uiStringsConfig}
    />
  ) : !sampleError ? (
    <SampleLoading uiStringsConfig={uiStringsConfig} />
  ) : fileNotFound ? (
    <FileNotFound uiStringsConfig={uiStringsConfig} />
  ) : (
    <SampleLoadingError uiStringsConfig={uiStringsConfig} />
  );
}

export function RedirectToSample() {
  const isPending = useIsSamplePending();
  const sample = useCurrentSample();
  const loadNewSample = useLoadNewSample();
  useEffect(() => {
    if (!isPending && sample === null) {
      loadNewSample();
    }
  }, [loadNewSample, sample, isPending]);

  if (sample !== null) {
    return (
      <Redirect
        to={{
          pathname: `/sample/${sample.id}`,
        }}
      />
    );
  }
  return null;
}

export function AnnotateSamplePage({
  children,
}: {
  children: React.ReactElement;
}) {
  const { sampleId } = useParams<{ sampleId: string }>();
  const sample = useCurrentSample();
  const isPending = useIsSamplePending();
  const loadNewSample = useLoadNewSample();
  useEffect(() => {
    if (!isPending && sample === null) {
      loadNewSample(sampleId);
    }
  }, [loadNewSample, sample, sampleId, isPending]);

  if (sample && sample.id !== sampleId) {
    return (
      <Redirect
        to={{
          pathname: `/sample/${sample.id}`,
        }}
      />
    );
  }

  return children;
}

export function AppContent() {
  const user = useUser();
  const samplesLeft = useSamplesLeft();
  const noInitialSamplesFound = useInitialSamplesFound();
  const annotationCount = useAnnotationCount();
  const uiStringsConfig = useUiStringsConfig();

  const performLogout = useLogoutAction();
  const { enqueueSnackbar } = useSnackbar();

  // TODO: Implement working logout here
  const handleLogout = async () => {
    await performLogout();
    enqueueSnackbar("Your login was successful.", {
      variant: "success",
    });
  };

  return user !== null ? (
    uiStringsConfig !== null ? (
      <UIChrome
        user={user}
        uiStringsConfig={uiStringsConfig}
        annotationCount={
          <AnnotationCountTable annotationCount={annotationCount} />
        }
        onLogout={handleLogout}
      >
        {" "}
        {noInitialSamplesFound ? (
          <NoInitialSamples uiStringsConfig={uiStringsConfig} />
        ) : !samplesLeft ? (
          <NoSamplesLeft uiStringsConfig={uiStringsConfig} />
        ) : (
          <Router>
            <Switch>
              <Route path="/(|sample)" exact>
                <RedirectToSample />
              </Route>
              <Route path="/sample/:sampleId" exact>
                <AnnotateSamplePage>
                  <AnnotationContent uiStringsConfig={uiStringsConfig} />
                </AnnotateSamplePage>
              </Route>
            </Switch>
          </Router>
        )}
      </UIChrome>
    ) : (
      <NoStringConfig />
    )
  ) : (
    <LoginScreen supportEmail={""} />
  );
}

export default function App() {
  return (
    <AppContext
      dependencies={{
        api: new BackendApi(),
      }}
    >
      <AppContent />
    </AppContext>
  );
}
