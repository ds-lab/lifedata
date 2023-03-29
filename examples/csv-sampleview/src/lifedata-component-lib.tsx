import React, { useEffect, useState } from "react"

interface SampleData {
  id: string
  data: any
}
type SampleViewArgs = any

enum ComponentMessageType {
  // Data: { apiVersion: number }
  // Only version 1 is supported at the moment.
  COMPONENT_READY = "lifedata:componentReady",

  // The component has a new height for its iframe.
  // Data: { height: number }
  SET_FRAME_HEIGHT = "lifedata:setFrameHeight",
}

enum FrameworkMessageType {
  RENDER = "lifedata:render",
}

export interface RenderData {
  id: string
  data: any
  args: any
}

class LIFEDATA {
  public static readonly API_VERSION = 1
  public static lastData: SampleData
  public static lastFrameHeight?: number
  public static registeredMessageListener: boolean = false
  public static readonly events = new EventTarget()

  /**
   * Report the component's height to LIFEDATA.
   * This should be called every time the component changes its DOM - that is,
   * when it's first loaded, and any time it updates.
   */
  public static setFrameHeight = (height?: number): void => {
    if (height === undefined) {
      // `height` is optional. If undefined, it defaults to scrollHeight,
      // which is the entire height of the element minus its border,
      // scrollbar, and margin.
      height = document.body.scrollHeight
    }

    if (height === LIFEDATA.lastFrameHeight) {
      // Don't bother updating if our height hasn't changed.
      return
    }

    LIFEDATA.lastFrameHeight = height
    LIFEDATA.sendBackMsg(ComponentMessageType.SET_FRAME_HEIGHT, { height })
  }

  private static onMessageEvent(event: MessageEvent): void {
    const type = event.data["type"]
    switch (type) {
      case FrameworkMessageType.RENDER:
        LIFEDATA.onRenderMessage(event.data)
        break
    }
  }

  private static onRenderMessage = (data: any): void => {
    let args = data["args"]
    if (args == null) {
      console.error(
        `Got null args in onRenderMessage. This should never happen`,
        data
      )
      args = {}
    }

    const eventData = { id: data.id, data: data.data, args }
    const event = new CustomEvent<RenderData>(FrameworkMessageType.RENDER, {
      detail: eventData,
    })
    LIFEDATA.events.dispatchEvent(event)
  }

  public static setComponentReady(): void {
    if (!LIFEDATA.registeredMessageListener) {
      // Register for message events if we haven't already
      window.addEventListener("message", LIFEDATA.onMessageEvent)
      LIFEDATA.registeredMessageListener = true
    }

    LIFEDATA.sendBackMsg(ComponentMessageType.COMPONENT_READY, {
      apiVersion: LIFEDATA.API_VERSION,
    })
  }

  private static sendBackMsg = (type: string, data?: any): void => {
    window.parent.postMessage(
      {
        isLifedataMessage: true,
        type: type,
        ...data,
      },
      "*"
    )
  }
}

interface SampleViewProps {
  id: string
  data: SampleData
  args: SampleViewArgs
  width: number
}

const ConnectSampleView = ({
  component: SampleViewComponent,
}: {
  component: React.ComponentType<SampleViewProps>
}) => {
  const [data, setData] = useState<SampleData | undefined>(undefined)
  const [args, setArgs] = useState({})
  const [width, setWidth] = useState(window.innerWidth)

  useEffect(() => {
    const listener = (event: Event) => {
      const renderData = (event as CustomEvent<RenderData>).detail

      setData({
        id: renderData.id,
        data: renderData.data,
      })
      setArgs(renderData.args)
    }

    LIFEDATA.events.addEventListener(FrameworkMessageType.RENDER, listener)
    LIFEDATA.setComponentReady()
    return () => {
      LIFEDATA.events.removeEventListener(FrameworkMessageType.RENDER, listener)
    }
  }, [])

  useEffect(() => {
    // Every time the component props update, we notify the framework of a
    // possible changed height.
    LIFEDATA.setFrameHeight()
  }, [data, args, width, SampleViewComponent])

  useEffect(() => {
    const listener = () => {
      setWidth(window.innerWidth)
    }
    window.addEventListener("resize", listener)
    return () => window.removeEventListener("resize", listener)
  })

  return data === undefined ? null : (
    <SampleViewComponent
      id={data.id}
      data={data.data}
      args={args}
      width={width}
    ></SampleViewComponent>
  )
}

export { ConnectSampleView }
