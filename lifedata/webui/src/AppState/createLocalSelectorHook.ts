import { useSelector } from "react-redux";

/**
 * Use this to create local useStateSelector hook selects the right subset of
 * state from the root based on `stateSelector`.
 *
 * For example if you have a reducer that is configured to put it's state at
 * the `user` property of the redux state, then you can create a
 * `useLocalSelector` hook with this function without knowing about the full
 * shape of the redux global state object:
 *
 *     interface UserState {
 *         loading: boolean,
 *         username: string | null,
 *         email: string | null,
 *     }
 *
 *     const useLocalSelector = createLocalSelectorHook((rootState: { user: UserState }) => rooState.user);
 *
 * Then you are decoupled from the shape of the global state object when
 * defining other selectors specific to your module:
 *
 *     export function useUserIsLoading() {
 *         return useLocalSelector((state: UserState) => state.loading);
 *     }
 */
export default function createLocalSelectorHook<
  TPartialRootState,
  TModuleState
>(globalStateSelector: (globalState: TPartialRootState) => TModuleState) {
  return function <TReturn>(
    localStateSelector: (state: TModuleState) => TReturn
  ) {
    return useSelector<TPartialRootState, TReturn>((globalState) =>
      localStateSelector(globalStateSelector(globalState))
    );
  };
}
