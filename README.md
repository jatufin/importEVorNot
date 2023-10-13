# importEVorNot

Helsinki University student project / Introduction to Data Science 2023

## Requesting, preprocessing and training

Information how to acquire new dataset can be found in the `nettiauto`directory.


## Starting the server locally:

* Update dependencies:
```
$ poetry install
```

* Launch the application
```
$ poetry run flask --app src/app.py run
```

* Open the application in browser: [http://localhost:5000/](http://localhost:5000/)

## API

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
$ URL = "{ 'url': 'https://mobile.de/...' }"
$ curl --request POST curl --header "Content-Type: application/json" --data $URL http://localhost:5000/predict
```

### `POST /predict`

Example:
```
$ INPUT_VECTOR = `cat query.json`
$ curl --request POST --header "Content-Type: application/json" --data $INPUT_VECTOR http://localhost:5000/predict
```

Returns the predicted value. (price)

