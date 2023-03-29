import React, { useEffect, useRef, useState } from "react";
import { Sample } from "../Sample";

/**
 * This component handles the rendering of a custom sample view. The sample
 * view is rendered as an iframe that shows the URL configured in
 * `get_sample_view` in `lifedata_api.py`.
 *
 * The communication with the page behind this URL is handled by sending and
 * receiving messages via `window.postMessage` and works like in the sequence
 * shown below:
 *
 *   CustomSampleView                                     Project-sample view
 *    (Annotation UI)                                         (in iframe)
 *
 *   - mounts iframe
 *
 *                                                        - loads and sends "componentReady" message
 *
 *                           <--- componentReady message -----
 *
 *   - sends sample data with "render" message
 *
 *                           --------- render message ------->
 *
 *                                                        - renders sample data, which might change height of component
 *                                                        - new height is reported
 *
 *                           <--- setFrameHeight message -----
 *
 *   - adjusts height of iframe
 *   - new sample arrives
 *
 *                           --------- render message ------->
 *
 *                                                        ...
 *
 */

enum MessageType {
  // Data: { apiVersion: number }
  // Only version 1 is supported at the moment.
  COMPONENT_READY = "lifedata:componentReady",

  // The component has a new height for its iframe.
  // Data: { height: number }
  SET_FRAME_HEIGHT = "lifedata:setFrameHeight",

  RENDER_EVENT = "lifedata:render",
}

const sendDataToComponent = (
  iframe: HTMLIFrameElement,
  sample: Sample,
  args: any
) => {
  iframe.contentWindow?.postMessage(
    {
      type: MessageType.RENDER_EVENT,
      id: sample.id,
      data: sample.data,
      args,
    },
    "*"
  );
};

export interface CustomSampleViewProps {
  sample: Sample;
  url: string;
  args: any;
}

export default function CustomSampleView({
  sample,
  url,
  args,
}: CustomSampleViewProps) {
  const [frameHeight, setFrameHeight] = useState(0);
  const [readyCount, setReadyCount] = useState(0);
  const ref = useRef<HTMLIFrameElement | null>(null);

  // Hook up message listener for iframe.
  useEffect(() => {
    if (ref.current === null) {
      return;
    }

    const iframe = ref.current;

    const messageListener = (event: MessageEvent) => {
      if (
        event.source !== iframe.contentWindow ||
        !event.data.isLifedataMessage
      ) {
        return;
      }

      if (event.data.type === MessageType.COMPONENT_READY) {
        if (event.data.apiVersion !== 1) {
          console.error(
            `Unsupported SampleView API_VERSION: ${event.data.apiVersion}`
          );
          return;
        }
        setReadyCount((c) => c + 1);
      }

      if (event.data.type === MessageType.SET_FRAME_HEIGHT) {
        setFrameHeight(event.data.height);
      }
    };

    window.addEventListener("message", messageListener);
    return () => window.removeEventListener("message", messageListener);
  }, [url]);

  // Send new sample data if either data changes or the iframe is ready to
  // receive data.
  useEffect(() => {
    if (readyCount > 0 && ref.current !== null) {
      sendDataToComponent(ref.current, sample, args || {});
    }
  }, [readyCount, sample, args]);

  return (
    <iframe
      src={url}
      key={url}
      style={{ height: frameHeight, width: "100%", border: "none" }}
      ref={ref}
      title={"custom sample view"}
    />
  );
}
