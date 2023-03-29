import React from "react";
import { render } from "@testing-library/react";

import App from "./App";

test("renders user name", () => {
  const { getByText } = render(<App />);
  const userElement = getByText(/Tester/i);
  expect(userElement).toBeInTheDocument();
});
