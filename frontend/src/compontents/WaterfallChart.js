import { useState } from 'react';
import Plot from 'react-plotly.js';
import { TextField }  from '@mui/material'

const WaterfallChart = ({ data: { purchasePrice, sellingPrice } }) => {

  const [otherExpenses, setOtherExpenses] = useState(3000);

  const titleText = purchasePrice+otherExpenses < sellingPrice 
    ? "This deal is your chance to make money!" 
    : "You should avoid this deal."

  const data = [
    {
        name: "Profit / loss",
        type: "waterfall",
        orientation: "v",
        measure: [
            "relative",
            "relative",
            "total",
            "relative",
            "total"
        ],
        x: [
            "Purchase",
            "Other expenses",
            "Total expenses",
            "Expected revenue",
            "Expected profit"
        ],
        textposition: "outside",
        text: [
            -purchasePrice,
            -otherExpenses,
            -purchasePrice-otherExpenses,
            sellingPrice,
            -purchasePrice-otherExpenses+sellingPrice
        ],          
        y: [
          -purchasePrice,
          -otherExpenses,
          0,
          sellingPrice,
          0
        ],
        connector: {
          line: {
            color: "rgb(63, 63, 63)"
          }
        },
        cliponaxis: false
    }
];
    const layout = {
        title: {
            text: titleText
        },
        xaxis: {
            type: "category",
            fixedrange: true,
        },
        yaxis: {
            type: "linear",
            fixedrange: true
        },
        autosize: true,
        showlegend: false,
        hovermode: false,
        font: {
          family: 'Montserrat, sans-serif',
        }
    };

    const config = {
      displayModeBar: false
    };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
      <div>
      <Plot
        data={data}
        layout={layout}
        config={config}
      />
      </div>
      <div style={{ marginTop: '-40px', marginBottom: '40px'}}>
      <TextField
        inputProps={{ step: "100" }}
        className="input"
        label="Other expenses"
        type="number"
        value={otherExpenses}
        onChange={(e) => setOtherExpenses(parseInt(e.target.value))}
      />
      </div>
    </div>
  );
};

export default WaterfallChart;
