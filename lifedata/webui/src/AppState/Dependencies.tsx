import { createContext, useContext } from "react";
import { IApi } from "../api";
import MockAPI from "../api/MockApi";

export interface AppDependencies {
  api: IApi;
}

export const defaultDependencies: AppDependencies = {
  api: new MockAPI(),
};

export const DependenciesContext = createContext(defaultDependencies);

export function useDependency<K extends keyof AppDependencies>(
  key: K
): AppDependencies[K] {
  const context = useContext(DependenciesContext);
  return context[key];
}
