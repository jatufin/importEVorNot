# importEVorNot

Helsinki University student project / Introduction to Data Science 2023

## Requesting, preprocessing and training

Information how to acquire new dataset can be found in the `nettiauto`directory.

## Starting the Backend server locally:

* Update dependencies:
```
$ poetry install
```

* Launch the application
```
$ poetry run flask --app src/app.py run
```

* API request can be directly to the server: `http://localhost:5000/


## Starting the Frontend server locally

```
$ npm start --prefix frontend
```

The application can be opened in a web browser: [http://localhost:3000/](http://localhost:3000/)


## Backend API

[http://localhost:5000/](http://localhost:5000/)

All reuqest except data in JSON format and return results in JSON.

### `GET /schema`

Example:
```
$ curl --request GET http://localhost:5000/schema
```
Returns the column (feature) names.

### `POST /fetch`

Produces the car information vector by wetching and parsing data from mobile.de. The data received from `/fetch` can used be directly for the `/predict` request.

```
$ URL_JSON = "{ 'url': 'https://mobile.de/...' }"
$ curl --request POST curl --header "Content-Type: application/json" --data $URL_JSON http://localhost:5000/predict
```

### `POST /predict`

Example:
```
$ VECTOR_JSON = `cat query.json`
$ curl --request POST --header "Content-Type: application/json" --data $VECTOR_JSON http://localhost:5000/predict
```

Returns the predicted value. (price)

