import Paper from "@material-ui/core/Paper"
import Table from "@material-ui/core/Table"
import TableBody from "@material-ui/core/TableBody"
import TableCell from "@material-ui/core/TableCell"
import TableContainer from "@material-ui/core/TableContainer"
import TableHead from "@material-ui/core/TableHead"
import TableRow from "@material-ui/core/TableRow"
import Papa from "papaparse"
import React from "react"

interface Props {
  id: string
  // This is dependent on the data format provided by `read_sample_for_display` in `lifedata_api.py`.
  data: any
  // Arguments can be passed via the `SampleView` configuration in
  // `lifedata_api.py` to statically configure the view.
  args: {}
  width: number
}

/**
 * This is a React-based sample view template. The data for the sample is
 * provided via `data`, integrate any HTML and react components you like to
 * display your sample data in the desired way.
 */

const CsvSampleView = ({ id, data: csvData, args, width }: Props) => {
  const parsedCsvdata = Papa.parse(csvData, { header: false })
  const rows = parsedCsvdata.data as Array<Array<string>>
  const header = rows[0]
  const body = rows.slice(1)

  return (
    <TableContainer component={Paper}>
      <Table size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            {header.map((cell, i) => (
              <TableCell key={i}>{cell}</TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {body.map((row, i) => (
            <TableRow key={i}>
              {row.map((cell, j) => (
                <TableCell key={`${i}-${j}`}>{cell}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  )
}

export default CsvSampleView
