import { createTheme } from "@material-ui/core/styles";

// Colors chosen based on https://material.io/resources/color/#!/?view.left=0&view.right=0&primary.color=03A9F4&secondary.color=FFCA28

export const BRAND = {
  background: "#040603",
  primary: "#03a9f4",
  secondary: "#ffca28",
  darkGrey: "#8c8c8c",
  lightGrey: "#bfbfbf",
};

export const brandTheme = createTheme({
  palette: {
    primary: {
      main: BRAND.background,
    },
  },
});
