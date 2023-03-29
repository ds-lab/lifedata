import React from "react";
import { Sample } from "../Sample";
import { SampleViewConfig } from "../SampleViewConfig";
import CustomSampleView, { CustomSampleViewProps } from "./CustomSampleView";
import Error from "./Error";
import ImageByUrlSampleView from "./ImageByUrlSampleView";

export type SampleViewComponentType = React.ComponentType<
  { sample: Sample; args: object } | CustomSampleViewProps
>;

export interface SampleViewProps {
  sample: Sample;
  args: object;
}

export default function SampleView({
  sample,
  config,
}: {
  sample: Sample;
  config: SampleViewConfig;
}) {
  if (typeof config.url === "string") {
    return (
      <CustomSampleView sample={sample} url={config.url} args={config.args} />
    );
  }

  switch (config.name) {
    case "error":
      return (
        <Error sample={sample} args={config.args as { message: string }} />
      );
    case "image-by-url":
      return <ImageByUrlSampleView sample={sample} args={config.args} />;
    default:
      return (
        <div>
          No SampleView component available with name <pre>{config.name}</pre>
        </div>
      );
  }
}
