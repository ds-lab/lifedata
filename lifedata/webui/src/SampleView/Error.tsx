import Alert from "@material-ui/lab/Alert";
import React from "react";
import { Sample } from "../Sample";

export default function Error({
  sample,
  args,
}: {
  sample: Sample;
  args: { message: string };
}) {
  return (
    <Alert severity="error">
      <strong>Cannot load SampleView:</strong> {args.message}
    </Alert>
  );
}
