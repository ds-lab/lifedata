import { createSlice } from "@reduxjs/toolkit";
import { useDispatch } from "react-redux";
import createLocalSelectorHook from "./createLocalSelectorHook";
import { useDependency } from "./Dependencies";
import { LabelConfig } from "../labels";
import { SampleViewConfig } from "../SampleViewConfig";
import { AnnotationQueueConfig } from "../queues";
import { StringConfig } from "../ui_strings";

type State = {
  sampleViewConfig: SampleViewConfig | null;
  labelConfig: LabelConfig | null;
  annotationQueueConfig: AnnotationQueueConfig | null;
  uiStringsConfig: StringConfig | null;
};

const initialState: State = {
  sampleViewConfig: null,
  labelConfig: null,
  annotationQueueConfig: null,
  uiStringsConfig: null,
};

const { actions, reducer } = createSlice({
  name: "project",
  initialState,
  reducers: {
    labelConfigLoaded: (state, { payload }: { payload: LabelConfig }) => {
      state.labelConfig = payload;
    },
    sampleViewConfigLoaded: (
      state,
      { payload }: { payload: SampleViewConfig }
    ) => {
      state.sampleViewConfig = payload;
    },
    annotationQueueConfigLoaded: (
      state,
      { payload }: { payload: AnnotationQueueConfig }
    ) => {
      state.annotationQueueConfig = payload;
    },
    uiStringsConfigLoaded: (state, { payload }: { payload: StringConfig }) => {
      state.uiStringsConfig = payload;
    },
  },
});

export default reducer;

const useLocalSelector = createLocalSelectorHook(
  (rootState: { project: State }) => rootState.project
);

export function useLabelConfig() {
  return useLocalSelector((state) => state.labelConfig);
}

export function useAnnotationQueueConfig() {
  return useLocalSelector((state) => state.annotationQueueConfig);
}

export function useUiStringsConfig() {
  return useLocalSelector((state) => state.uiStringsConfig);
}

export function useSampleViewConfig() {
  return useLocalSelector((state) => state.sampleViewConfig);
}

export function useLoadLabelConfig() {
  const dispatch = useDispatch();
  const api = useDependency("api");

  return async () => {
    const labelConfig = await api.getLabels();
    dispatch(actions.labelConfigLoaded(labelConfig));
  };
}

export function useLoadUiStringsConfig() {
  const dispatch = useDispatch();
  const api = useDependency("api");

  return async () => {
    const string_config = await api.getUiStrings();
    dispatch(actions.uiStringsConfigLoaded(string_config));
  };
}

export function useLoadAnnotationQueueConfig() {
  const dispatch = useDispatch();
  const api = useDependency("api");

  return async () => {
    const annotationQueuesConfig = await api.getAnnotationQueueConfig();
    dispatch(actions.annotationQueueConfigLoaded(annotationQueuesConfig));
  };
}

export function useLoadSampleViewConfig() {
  const dispatch = useDispatch();
  const api = useDependency("api");

  return async () => {
    const sampleViewConfig = await api.getSampleViewConfig();
    dispatch(actions.sampleViewConfigLoaded(sampleViewConfig));
  };
}
