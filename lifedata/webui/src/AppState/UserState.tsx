import { createSlice } from "@reduxjs/toolkit";
import { useMemo } from "react";
import { useDispatch } from "react-redux";
import { User } from "../User";
import createLocalSelectorHook from "./createLocalSelectorHook";
import { useDependency } from "./Dependencies";

type State = {
  user: User | null;
};

const initialState: State = { user: null };

const { actions, reducer } = createSlice({
  name: "user",
  initialState,
  reducers: {
    loggedIn: (state, { payload }: { payload: User }) => {
      state.user = payload;
    },
    loggedOut: (state) => {
      state.user = null;
    },
  },
});

export default reducer;

const useLocalSelector = createLocalSelectorHook(
  (rootState: { user: State }) => rootState.user
);

export function useUser() {
  return useLocalSelector((state) => state.user);
}

export function useLogin() {
  const dispatch = useDispatch();
  const api = useDependency("api");

  return useMemo(() => {
    return async (token: string) => {
      const user = await api.authenticate(token);
      dispatch(actions.loggedIn(user));
    };
  }, [dispatch, api]);
}

export function useLogoutAction() {
  const dispatch = useDispatch();
  const api = useDependency("api");

  return async () => {
    api.logout();
    dispatch(actions.loggedOut());
  };
}
