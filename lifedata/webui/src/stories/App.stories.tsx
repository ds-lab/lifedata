import React, { useEffect } from "react";
import { AnnotationContent, AppContent } from "../App";
import MockAppContext from "../MockAppContext";
import { useLoadNewSample } from "../AppState/SampleState";
import testSample1 from "./test_sample_01.json";
import { Sample } from "../Sample";
import exampleStringConfig from "../stories/test_string_config.json";

export default {
  title: "App (with fake state)",
};

function InitSamplePage({
  exampleSample,
  children,
}: {
  exampleSample: Sample;
  children: React.ReactElement;
}) {
  const sampleId = exampleSample.id;
  const loadNewSample = useLoadNewSample();
  useEffect(() => {
    loadNewSample(sampleId);
  }, [loadNewSample, sampleId]);

  return children;
}

export const Default = () => {
  return (
    <MockAppContext>
      <InitSamplePage exampleSample={testSample1}>
        <AnnotationContent uiStringsConfig={exampleStringConfig} />
      </InitSamplePage>
    </MockAppContext>
  );
};

export const SlowConnection = () => {
  return (
    <MockAppContext
      mockOptions={{
        delay: 1500,
      }}
    >
      <InitSamplePage exampleSample={testSample1}>
        <AnnotationContent uiStringsConfig={exampleStringConfig} />
      </InitSamplePage>
    </MockAppContext>
  );
};

export const FailOnAuthenticate = () => {
  return (
    <MockAppContext
      mockOptions={{
        failOnAuthenticate: true,
      }}
    >
      <InitSamplePage exampleSample={testSample1}>
        <AnnotationContent uiStringsConfig={exampleStringConfig} />
      </InitSamplePage>
    </MockAppContext>
  );
};

export const FailOnLoadSample = () => {
  return (
    <MockAppContext
      mockOptions={{
        failOnLoadSample: true,
      }}
    >
      <InitSamplePage exampleSample={testSample1}>
        <AnnotationContent uiStringsConfig={exampleStringConfig} />
      </InitSamplePage>
    </MockAppContext>
  );
};

export const NoSamplesLeft = () => {
  return (
    <MockAppContext
      mockOptions={{
        samplesLeft: false,
      }}
    >
      <InitSamplePage exampleSample={testSample1}>
        <AppContent />
      </InitSamplePage>
    </MockAppContext>
  );
};

export const NoInitialSamplesFound = () => {
  return (
    <MockAppContext
      mockOptions={{
        noInitialSamplesFound: true,
      }}
    >
      <InitSamplePage exampleSample={testSample1}>
        <AppContent />
      </InitSamplePage>
    </MockAppContext>
  );
};

export const NoFileFound = () => {
  return (
    <MockAppContext
      mockOptions={{
        fileNotFound: true,
      }}
    >
      <InitSamplePage exampleSample={testSample1}>
        <AnnotationContent uiStringsConfig={exampleStringConfig} />
      </InitSamplePage>
    </MockAppContext>
  );
};

export const FailOnSubmit = () => {
  return (
    <MockAppContext
      mockOptions={{
        failOnSubmitSample: true,
      }}
    >
      <InitSamplePage exampleSample={testSample1}>
        <AnnotationContent uiStringsConfig={exampleStringConfig} />
      </InitSamplePage>
    </MockAppContext>
  );
};
