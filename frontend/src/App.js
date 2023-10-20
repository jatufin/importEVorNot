import { useState } from "react"
import axios from "axios"
import { Formik, Form, Field } from "formik"

const Title = () => (
    <h1>importEVorNot</h1>
)

const UrlForm = ({ onSubmit, url, onUrlChange }) => (
        <form onSubmit={onSubmit}>
        <label>Paste the URL here</label>
        <input value={url} onChange={onUrlChange} />
        <button type="submit">Fetch</button>
        </form>
)

const Message = ({ value }) => (
        <div>{value}</div>
)

const Image = ({ src, alt, width }) => (
    src ? <img src={src} alt={alt} width={width} /> : ""
)

const CarForm = ({ initialValues }) => {
    if (initialValues === undefined || Object.keys(initialValues).length === 0) {
        return
    }

    var fields = []
    for (const key in initialValues) {
        const value = initialValues[key]
        const data_type = typeof(value)

        let input_type = ""
        switch (data_type) {
        case "boolean":
            input_type="checkbox"
            break
        case "number":
            input_type="number"
            break
        default:
            input_type="text"
        }

        fields.push(
                <div key={key}>
                <label htmlFor={key}>{key}</label>
                <Field id={key} name={key} type={input_type} />
                <br />
                </div>
        )
    }

    return(
            <Form>
            <button type="submit">Calculate the predicted price in Finland</button>
            {fields}
        </Form>
    )
}

function App() {
    const [url, setUrl] = useState("")
    const [message, setMessage] = useState("")
    const [formData, setFormData] = useState({})
    const [carImageUrl, setCarImageUrl] = useState("")
    
    const fetchFromMobile = (event) => {
        event.preventDefault()

        setMessage("Fetching data from Mobile...")
        
        axios
            .post("http://localhost:5000/fetch", { "url": url })
            .then(response => {
                setFormData(response.data.car_data)
                setCarImageUrl(response.data.img_url)
                setMessage("Success!")
            })
            .catch(error => setMessage(error.response.data))
        setUrl("")
    }
    
    const submitForm = (values) => {
        console.log(values)
        
        axios
            .post("http://localhost:5000/predict", { "query": values })
            .then(response => setMessage("Predicted price: " + response.data.prediction.price))
            .catch(error => setMessage(error.response.data))
    }
    
    const urlChangeHandler = (event) => { setUrl(event.target.value); setMessage("") }

    return (
            <div>
            <Title />
            <UrlForm url={url} onSubmit={fetchFromMobile} onUrlChange={urlChangeHandler} />
            <Message value={message} />

            <Formik initialValues={formData} onSubmit={submitForm} enableReinitialize={true}>
            <CarForm initialValues={formData} />
            </Formik>
            
            <Image src={carImageUrl} alt="car" width="500" />
            </div>
    )
}

export default App;
