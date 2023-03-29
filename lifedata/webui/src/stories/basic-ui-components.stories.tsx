import React from "react";
import { action } from "@storybook/addon-actions";
import Button from "@material-ui/core/Button";
import HeaderAppBar from "../HeaderAppBar";
import testUser01 from "./test_user_01.json";
import { AnnotationCountTable } from "../AnnotationCountTable";
import exampleAnnotationCountConfig from "../stories/test_annotation_count.json";
import exampleStringConfig from "../stories/test_string_config.json";

export default {
  title: "Basic UI Components",
  component: Button,
};

export const ButtonDefault = () => (
  <Button variant="contained" onClick={action("clicked")}>
    Hello Button
  </Button>
);

export const Header = () => (
  <HeaderAppBar
    user={testUser01}
    uiStringsConfig={exampleStringConfig}
    annotationCount={
      <AnnotationCountTable annotationCount={exampleAnnotationCountConfig} />
    }
    onLogout={action("logged out")}
  />
);
