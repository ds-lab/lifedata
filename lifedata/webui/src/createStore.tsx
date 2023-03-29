import React, { createContext, useContext, useReducer } from "react";

export default function createStore<
  State extends {},
  Actions extends {},
  Dependencies extends {} = {}
>(
  initialState: State,
  reducer: (state: State, action: Actions) => State,
  defaultDependencies: Dependencies
) {
  const StoreContext = createContext<{
    state: State;
    dispatch: (action: Actions) => void;
    dependencies: Dependencies;
  }>({
    state: initialState,
    dispatch: (action: Actions) => null,
    dependencies: defaultDependencies,
  });

  function useState() {
    const { state } = useContext(StoreContext);
    return state;
  }

  function useDispatch() {
    const { dispatch } = useContext(StoreContext);
    return dispatch;
  }

  function useDependency() {
    const { dependencies } = useContext(StoreContext);
    return dependencies;
  }

  function Provider({
    children,
    dependencies,
  }: {
    children: React.ReactNode;
    dependencies?: Partial<Dependencies>;
  }) {
    const [state, dispatch] = useReducer(reducer, initialState);
    const concreteDependencies = {
      ...defaultDependencies,
      ...dependencies,
    };

    return (
      <StoreContext.Provider
        value={{ state, dispatch, dependencies: concreteDependencies }}
      >
        {children}
      </StoreContext.Provider>
    );
  }

  return {
    Provider,
    useState,
    useDispatch,
    useDependency,
  };
}
