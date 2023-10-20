import { useState } from "react"
import axios from "axios"
import { Formik, Form, Field } from "formik"

const Title = () => (
    <h1>importEVorNot</h1>
)

///////////////////
// The form where user copies the mobile.de ad address
const UrlForm = ({ onSubmit, url, onUrlChange }) => (
        <form onSubmit={onSubmit}>
        <input value={url} onChange={onUrlChange} />
        <button type="submit">Fetch</button>
        </form>
)

///////////////////
// After the backend has fetch the data from mobile.de, it appears here
// The user should not be able to edit this manually
const QueryForm = ({ onSubmit, query, onQueryChange }) => (
        <form onSubmit={onSubmit} >
        <input value={query} onChange={onQueryChange} />
        <button type="submit">Predict</button>
        </form>
)


///////////////////
// Here is the prediction shown after it has been acquired from the backend
const Message = ({ value }) => (
        <div>{value}</div>
)

const Image = ({ src, alt, width }) => (
        <img src={src} alt={alt} width={width} />
)

const CarForm = ({ initialValues }) => {
    if (initialValues == undefined) {
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

        // console.log("Key: " + key +  "Value: " + value + " Type: " + typeof(value) + " Input type: " + input_type)
        fields.push(
                <div key={key}>
                <label htmlFor={key}>{key}</label>
                <Field id={key} name={key} type={input_type} />
                <br />
                </div>
        )
    }

    return(<Form>{fields}<button type="submit">Submit</button></Form>)
}
function App() {
    const [url, setUrl] = useState("")
    const [query, setQuery] = useState("")
    const [message, setMessage] = useState("")
    const [carImageUrl, setCarImageUrl] = useState("")

    const [formData, setFormData] = useState({})
    
    const fetchFromMobile = (event) => {
        event.preventDefault()

        setMessage("Fetching data from Mobile...")
        
        axios
            .post("http://localhost:5000/fetch", { "url": url })
            .then(response => {
                setQuery(JSON.stringify(response.data.car_data))
                setFormData(response.data.car_data)
                setCarImageUrl(response.data.img_url)
                setMessage("Success!")
            })
            .catch(error => setMessage(error.response.data))
        setUrl("")
    }

    const predict = (event) => {
        event.preventDefault()

        axios
            .post("http://localhost:5000/predict", { "query": JSON.parse(query) })
            .then(response => setMessage("Predicted price: " + response.data.prediction.price))
            .catch(error => setMessage(error.response.data))
    }
    
    const submitForm = (values) => {
        console.log(values)
        
        axios
            .post("http://localhost:5000/predict", { "query": values })
            .then(response => setMessage("Predicted price: " + response.data.prediction.price))
            .catch(error => setMessage(error.response.data))
    }
    
    const urlChangeHandler = (event) => { setUrl(event.target.value); setMessage("") }
    const queryChangeHandler = (event) => { setQuery(event.target.value); setMessage("") }

    return (
            <div>
            <Title />
            <UrlForm url={url} onSubmit={fetchFromMobile} onUrlChange={urlChangeHandler} />
            <QueryForm query={query} onSubmit={predict} onQueryChange={queryChangeHandler} />
            <Message value={message} />
            {carImageUrl ? <Image src={carImageUrl} alt="car" width="500" /> : ""}
        
            <Formik initialValues={formData} onSubmit={submitForm} enableReinitialize={true}>
            <CarForm initialValues={formData} />
            </Formik>
            
            </div>
    )
}

export default App;
