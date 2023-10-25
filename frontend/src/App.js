import { useState } from "react";
import axios from "axios";
import { Formik, Form, Field } from "formik";
import classNames from "classnames";

import { Button, TextField, FormControlLabel, Checkbox, CircularProgress } from "@mui/material";

import "./style.scss";
import WaterfallChart from "./compontents/WaterfallChart";

const allowedFields = new Set([
  "power",
  "batteryCapacity",
  "kilometers",
  "totalOwners",
]);

const Title = () => <h1>importEVorNot</h1>;

const UrlForm = ({ onNewData, onLoading }) => {
  const [url, setUrl] = useState(
    "https://suchen.mobile.de/fahrzeuge/details.html?id=371685965&cn=DE&fuels=ELECTRICITY&isSearchRequest=true&pageNumber=1&scopeId=C&sortOption.sortBy=creationTime&sortOption.sortOrder=DESCENDING&action=topOfPage&top=1:1&searchId=856659eb-7a56-6dcf-7214-894d377b468c&ref=srp"
  );
  const handleInputChange = (event) => {
    setUrl(event.target.value);
  };

  const fetchFromMobile = (event) => {
    event.preventDefault();
    onLoading()

    axios.post("/fetch", { url: url }).then((response) => {
      onNewData(response.data);
    });
    // .catch(error => setMessage(error.response.data))
  };

  return (
    <form onSubmit={fetchFromMobile}>
      <TextField
        className="input"
        placeholder="Paste the URL here"
        value={url}
        onChange={handleInputChange}
      />
      <Button type="submit">Fetch</Button>
    </form>
  );
};

const resolveInputType = (input_type) => {
  switch (typeof input_type) {
    case "boolean":
      return "checkbox";
    case "number":
      return "number";
    default:
      return "text";
  }
};

const formatLabel = (key) => {
  key = key.replaceAll("_", " ");
  return Array.from(key)
    .map((c) => (c.charCodeAt(0) >= 97 ? c : ` ${c}`.toLowerCase()))
    .join("")
    .trim();
};

const CarForm = ({ formData, onSubmit }) => {
  const fields = Object.entries(formData).map(([key, value]) => [
    key,
    value,
    resolveInputType(value),
  ]);
  const basicDetails = fields
    .filter((x) => x[2] !== "checkbox")
    .map(([key, value, inputType]) => {
      return (
        <div className={classNames("input-group", inputType)} key={key}>
          <Field id={key} name={key} type={resolveInputType(value)}>
            {({ field }) => (
              <TextField
                fullWidth
                label={formatLabel(key)}
                type={inputType}
                {...field}
                
                disabled={!allowedFields.has(key)}
              />
            )}
          </Field>
        </div>
      );
    });

  const extras = fields
    .filter((x) => x[2] === "checkbox")
    .map(([key, value, inputType]) => {
      return (
        <div className={classNames("input-group", inputType)} key={key}>
          <Field id={key} name={key} type={resolveInputType(value)}>
            {({ field }) => {
              return (
                <FormControlLabel
                  control={<Checkbox fullWidth {...field} />}
                  label={formatLabel(key)}
                />
              );
            }}
          </Field>
        </div>
      );
    });

  return (
    <div className="car-detail-form">
      <Formik
        initialValues={formData}
        onSubmit={onSubmit}
        enableReinitialize={true}
      >
        <Form>
          <div className="car-detail-submit">
            <Button type="submit" variant="contained">
              Get prediction
            </Button>
          </div>

          <h2>Basic details</h2>

          <div className="car-detail-inputs">{basicDetails}</div>

          <h2>Extras</h2>

          <div className="car-detail-extras">{extras}</div>
        </Form>
      </Formik>
    </div>
  );
};



const CarAnalytics = ({ prediction, original_price }) => {
  return (
    <div className="car-analytics-section">
      <p>
        Price in Finland about <b>{prediction.price}</b> €
      </p> 
      <WaterfallChart data = {{
        "purchasePrice" : original_price,
        "sellingPrice" : prediction.price
      }}/>
    </div>
  );
};

function App() {
  const [formData, setFormData] = useState();
  const [carImageUrl, setCarImageUrl] = useState("");
  const [prediction, setPrediction] = useState();
  const [loading, setLoading] = useState(false)

  const handleNewCarData = (data) => {
    if (data) {
      setFormData(data.car_data);
      setCarImageUrl(data.img_url);
    }
    setLoading(false);
    setPrediction();
  };

  const hadleNewCarDataLoading = () => {
    setLoading(true)
  }

  const submitForm = (values) => {
    axios
      .post("/predict", { query: values })
      .then((response) => setPrediction(response.data));
    // .catch(error => setMessage(error.response.data))
  };

  return (
    <div className="app">
      <div
        className={classNames("search-container", {
          "padding-top-30vh": !formData,
        })}
      >
        <Title />
        <UrlForm onNewData={handleNewCarData} onLoading={hadleNewCarDataLoading} />

        {loading && <CircularProgress className="p-1" />}
      </div>

      {carImageUrl && (
        <div className="car-image-section">
          <div className="car-image-wrapper">
            <img src={carImageUrl} alt={`${formData.make} ${formData.model}`} />
          </div>
        </div>
      )}

      {prediction && <CarAnalytics {...prediction} />}

      {formData && (
        <CarForm
          formData={formData}
          onSubmit={submitForm}
          carImageUrl={carImageUrl}
        />
      )}
    </div>
  );
}

export default App;
