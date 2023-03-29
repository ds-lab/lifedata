import { configureStore } from "@reduxjs/toolkit";
import React, { useEffect } from "react";
import { Provider } from "react-redux";
import {
  AppDependencies,
  defaultDependencies,
  DependenciesContext,
} from "./Dependencies";
import projectReducer, {
  useLoadLabelConfig,
  useLoadSampleViewConfig,
  useLoadAnnotationQueueConfig,
  useLoadUiStringsConfig,
} from "./ProjectState";
import sampleReducer from "./SampleState";
import userReducer, { useLogin, useUser } from "./UserState";
import { useSnackbar } from "notistack";

let store = initStore();

function initStore() {
  return configureStore({
    reducer: {
      sample: sampleReducer,
      user: userReducer,
      project: projectReducer,
    },
  });
}

export function resetStore() {
  store = initStore();
}

const Bootstrap = React.memo(({ children }: { children: React.ReactNode }) => {
  const login = useLogin();
  const user = useUser();
  const loadLabelConfig = useLoadLabelConfig();
  const loadSampleViewConfig = useLoadSampleViewConfig();
  const loadAnnotationQueueConfig = useLoadAnnotationQueueConfig();
  const loadUiStringConfig = useLoadUiStringsConfig();
  const snackbar = useSnackbar();

  // TODO: Remove this useEffect cause it is never used due to the keycloack usage
  useEffect(() => {
    const fail = () => {
      snackbar.enqueueSnackbar(
        "Sorry, your login details where not correct. Please make sure to enter correct username and password.",
        { variant: "error", persist: true }
      );
    };
    const token = "TT";
    login(token).catch(() => {
      fail();
    });
  }, [login, snackbar]);

  // TODO: Find out when this is used and maybe extract string
  useEffect(() => {
    const fail = () => {
      snackbar.enqueueSnackbar(
        "Sorry, the page cannot be loaded. Please try again by refreshing the page.",
        { variant: "error", persist: true }
      );
    };

    loadLabelConfig().catch(() => {
      fail();
    });
    loadSampleViewConfig().catch(() => {
      fail();
    });
    loadAnnotationQueueConfig().catch(() => {
      fail();
    });
    loadUiStringConfig().catch(() => {
      fail();
    });
  }, [
    loadLabelConfig,
    loadSampleViewConfig,
    loadAnnotationQueueConfig,
    loadUiStringConfig,
    snackbar,
  ]);

  if (user !== null) {
    return <>{children}</>;
  }
  return null;
});

export function AppStateProvider({
  dependencies = defaultDependencies,
  children,
}: {
  dependencies?: AppDependencies;
  children: React.ReactNode;
}) {
  return (
    <DependenciesContext.Provider value={dependencies}>
      <Provider store={store}>
        <Bootstrap>{children}</Bootstrap>
      </Provider>
    </DependenciesContext.Provider>
  );
}
