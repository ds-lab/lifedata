import React, { ReactNode, useEffect } from "react";
import MockAPI, { MockAPIOptions } from "./api/MockApi";
import { AppContext } from "./App";
import { resetStore } from "./AppState/AppState";

export default function MockAppContext({
  children,
  mockOptions,
}: {
  children: ReactNode;
  mockOptions?: MockAPIOptions;
}) {
  useEffect(() => {
    resetStore();
  });

  return (
    <AppContext
      dependencies={{
        api: new MockAPI(mockOptions),
      }}
    >
      {children}
    </AppContext>
  );
}
