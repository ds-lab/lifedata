import { createSlice } from "@reduxjs/toolkit";
import { useMemo } from "react";
import { useDispatch } from "react-redux";
import { Label } from "../labels";
import { Sample } from "../Sample";
import createLocalSelectorHook from "./createLocalSelectorHook";
import { useDependency } from "./Dependencies";
import { AnnotationCountDefinition } from "../counts";
import { QueuedSamples } from "../queues";

type State = {
  sample: Sample | null;
  annotationCount: AnnotationCountDefinition | null;
  loading: boolean;
  error: boolean;
  submitting: boolean;
  submitError: boolean;
  samplesLeft: boolean;
  noInitialSamplesFound: boolean;
  fileNotFound: boolean;
  queuedSamples: QueuedSamples | null;
};

const initialState: State = {
  sample: null,
  annotationCount: null,
  loading: false,
  error: false,
  submitting: false,
  submitError: false,
  samplesLeft: true,
  noInitialSamplesFound: false,
  fileNotFound: false,
  queuedSamples: null,
};

const slice = createSlice({
  name: "sample",
  initialState,
  reducers: {
    loadingStarted: (state) => {
      state.error = false;
      state.sample = null;
      state.annotationCount = null;
      state.loading = true;
      state.samplesLeft = true;
      state.fileNotFound = false;
      state.noInitialSamplesFound = false;
    },
    update_annotation_count: (
      state,
      { payload }: { payload: AnnotationCountDefinition }
    ) => {
      state.annotationCount = payload;
    },
    update_queued_samples: (state, { payload }: { payload: QueuedSamples }) => {
      state.queuedSamples = payload;
    },

    loadingFinished: (state, { payload }: { payload: Sample }) => {
      state.sample = payload;
      state.loading = false;
    },
    loadingFailed: (state) => {
      state.loading = false;
      state.error = true;
    },
    noSamplesLeft: (state) => {
      state.sample = null;
      state.loading = false;
      state.samplesLeft = false;
    },
    noInitialSamples: (state) => {
      state.noInitialSamplesFound = true;
    },
    fileNotFound: (state) => {
      state.sample = null;
      state.loading = false;
      state.error = true;
      state.fileNotFound = true;
    },
    submitStarted: (state) => {
      state.submitting = true;
      state.submitError = false;
    },
    submitFinished: (state) => {
      state.submitting = false;
    },
    submitFailed: (state) => {
      state.submitting = false;
      state.submitError = true;
    },
  },
});

const { actions, reducer } = slice;

export default reducer;

const useLocalSelector = createLocalSelectorHook(
  (rootState: { sample: State }) => rootState.sample
);

export function useSubmitSample() {
  const dispatch = useDispatch();
  const sample = useCurrentSample();
  const loadNewSample = useLoadNewSample();
  const api = useDependency("api");

  return async (labels: Label[]) => {
    if (sample === null) {
      return;
    }

    dispatch(actions.submitStarted());
    try {
      await api.submitSample(sample, labels);
      dispatch(actions.submitFinished());
      await loadNewSample();
    } catch (e) {
      dispatch(actions.submitFailed());
      throw e;
    }
  };
}

export function useConsultColleague() {
  const dispatch = useDispatch();
  const sample = useCurrentSample();
  const loadNewSample = useLoadNewSample();
  const api = useDependency("api");

  return async (queue_name: string, labels: Label[]) => {
    if (sample === null) {
      return;
    }
    dispatch(actions.submitStarted());
    try {
      await api.consultColleague(sample, queue_name, labels);
      dispatch(actions.submitFinished());
      loadNewSample();
    } catch (e) {
      dispatch(actions.submitFailed());
      throw e;
    }
  };
}

export function useSkipSample() {
  const dispatch = useDispatch();
  const sample = useCurrentSample();
  const loadNewSample = useLoadNewSample();
  const api = useDependency("api");

  return async () => {
    if (sample === null) {
      return;
    }

    dispatch(actions.submitStarted());
    try {
      await api.skipSample(sample);
      dispatch(actions.submitFinished());
      await loadNewSample();
    } catch (e) {
      dispatch(actions.submitFailed());
      throw e;
    }
  };
}

export function useLoadNewSample() {
  const dispatch = useDispatch();
  const api = useDependency("api");

  return useMemo(() => {
    return async (sampleId?: string) => {
      dispatch(actions.loadingStarted());
      try {
        let nextSample;
        let actual_annotation_count = await api.getAnnotationCount();
        const annotation_count = actual_annotation_count;
        let actual_queued_samples = await api.getQueuedSamples();
        const queued_samples = actual_queued_samples;
        dispatch(actions.update_annotation_count(annotation_count));
        dispatch(actions.update_queued_samples(queued_samples));
        if (sampleId !== undefined) {
          nextSample = await api.getSampleByID(sampleId);
        } else {
          nextSample = await api.getCurrentSample();
        }
        if (nextSample.status === "no-samples-left") {
          dispatch(actions.noSamplesLeft());
        } else if (nextSample.status === "no-initial-samples") {
          dispatch(actions.noInitialSamples());
        } else if (nextSample.status === "sample-not-found") {
          dispatch(actions.fileNotFound());
        } else {
          const sample = nextSample.sample as Sample;
          dispatch(actions.loadingFinished(sample));
        }
      } catch (e) {
        dispatch(actions.loadingFailed());
      }
    };
  }, [dispatch, api]);
}

export function useSamplesLeft() {
  return useLocalSelector((state) => state.samplesLeft);
}

export function useInitialSamplesFound() {
  return useLocalSelector((state) => state.noInitialSamplesFound);
}

export function useCurrentSample() {
  return useLocalSelector((state) => state.sample);
}

export function useQueuedSamples() {
  return useLocalSelector((state) => state.queuedSamples);
}

export function useAnnotationCount() {
  return useLocalSelector((state) => state.annotationCount);
}

export function useIsSampleLoading() {
  return useLocalSelector((state) => state.loading);
}

export function useHasSampleError() {
  return useLocalSelector((state) => state.error);
}

export function useFileNotFound() {
  return useLocalSelector((state) => state.fileNotFound);
}

/**
 * A selector hook to determine whether a sample is either currently
 * loading or cannot be loaded due to different errors.
 * In other words: It is *not* pending either if it no sample has been requested
 * yet, or the sample has successfully loaded.
 */
export function useIsSamplePending() {
  return useLocalSelector((state) => {
    return (
      (state.error || state.loading || state.samplesLeft === false) &&
      state.sample === null
    );
  });
}

export function useIsSubmitting() {
  return useLocalSelector((state) => state.submitting);
}

export function useSubmitError() {
  return useLocalSelector((state) => state.submitError);
}
