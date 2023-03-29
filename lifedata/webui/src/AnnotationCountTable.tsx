import { AnnotationCountDefinition } from "./counts";
import React from "react";

export function AnnotationCountTable({
  annotationCount,
}: {
  annotationCount: AnnotationCountDefinition | null;
}) {
  return annotationCount == null ? (
    <div></div>
  ) : (
    <div style={{ color: "white" }}>
      <table>
        <tbody>
          <tr>
            <td>Overall annotations:</td>
            <td>{annotationCount.overall}</td>
          </tr>
          <tr>
            <td>Monthly annotations:</td>
            <td>{annotationCount.monthly}</td>
          </tr>
          <tr>
            <td>Weekly annotations:</td>
            <td>{annotationCount.weekly}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
