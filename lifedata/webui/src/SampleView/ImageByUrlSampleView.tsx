import React from "react";
import { Container } from "@material-ui/core";
import { Sample } from "../Sample";

export default function SampleView({
  sample,
  args,
}: {
  sample: Sample;
  args: object;
}) {
  return (
    <Container style={{ textAlign: "center" }}>
      <img src={sample.data} alt={sample.id} />
    </Container>
  );
}
