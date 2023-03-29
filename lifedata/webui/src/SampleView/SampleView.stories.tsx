import React from "react";
import SampleView from "./SampleView";
import CustomSampleView from "./CustomSampleView";
import sampleSample from "../stories/test_sample_01.json";
import Alert from "@material-ui/lab/Alert";

export default {
  title: "Sample View",
  component: SampleView,
};

export const ImageByUrlSampleView = () => (
  <SampleView
    sample={sampleSample}
    config={{ name: "image-by-url", args: {} }}
  />
);

const csvSampleSample = {
  id: "csv01",
  data: `\
A,B
1.0,1.5
2.0,3.5`,
};

export const ExternalSampleView = () => (
  <div>
    <Alert severity="info">
      Make sure to have a sample view dev-server running at localhost:3010. E.g.
      start with <code>yarn install ; yarn run start</code> in the{" "}
      <code>examples/csv-sampleview</code> directory.
    </Alert>
    <CustomSampleView
      url={"http://localhost:3010"}
      sample={csvSampleSample}
      args={{ name: "foo" }}
    />
  </div>
);
