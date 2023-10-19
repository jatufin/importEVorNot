import { useState } from "react"
import axios from "axios"

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

function App() {
    const [url, setUrl] = useState("")
    const [query, setQuery] = useState("")
    const [message, setMessage] = useState("")
    
    const fetchFromMobile = (event) => {
        event.preventDefault()
        
        axios
            .post("http://localhost:5000/fetch", { "url": url })
            .then(response => setQuery(JSON.stringify(response.data)))
            .catch(error => setMessage("There was a problem with fetching the advertisement."))
        setUrl("")
    }

    const predict = (event) => {
        event.preventDefault()

        axios
            .post("http://localhost:5000/predict", { "query": JSON.parse(query) })
            .then(response => setMessage("Predicted price: " + response.data.prediction.price))
            .catch(error => setMessage("There was a problem with making the prediction."))
    }
    
    const urlChangeHandler = (event) => setUrl(event.target.value)
    const queryChangeHandler = (event) => setQuery(event.target.value)
    
    return (
            <div>
            <Title />
            <UrlForm url={url} onSubmit={fetchFromMobile} onUrlChange={urlChangeHandler} />
            <QueryForm query={query} onSubmit={predict} onQueryChange={queryChangeHandler} />
            <Message value={message} />
            </div>
    )
}

export default App;
