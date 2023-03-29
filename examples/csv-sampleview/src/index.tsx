import React from "react"
import ReactDOM from "react-dom"
import { ConnectSampleView } from "./lifedata-component-lib"
import CsvSampleView from "./CsvSampleView"

ReactDOM.render(
  <React.StrictMode>
    {/* "ConnectSampleView" is a wrapper component that bootstraps the connection
    between your component and the LIFEDATA annotation interface. */}
    <ConnectSampleView component={CsvSampleView} />
  </React.StrictMode>,
  document.getElementById("root")
)
